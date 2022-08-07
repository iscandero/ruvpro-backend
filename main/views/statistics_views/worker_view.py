from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.authentication import AppUserAuthentication
from main.const_data.template_errors import USER_NOT_FOUND_DATA
from main.serializers.statistics_serializers.perosnal_serializers import WorkTimeSerializerForStatistics, \
    RateSerializerForStatistics, SalarySerializerForStatistics
from main.services.statistic.selectors import get_time_entry_by_user_and_interval_date, \
    get_rate_by_user_and_interval_date_with_need_currency, get_current_avg_worker_rate_by_user_with_need_currency
from main.services.statistic.use_cases import get_entries_to_salary_chart

from main.services.work_with_date import convert_timestamp_to_date


class GetWorkerStatistic(APIView):
    authentication_classes = [AppUserAuthentication]

    def get(self, request):
        user = request.user
        if user:
            start_date_timestamp = float(request.headers.get('startDate'))
            end_date_timestamp = float(request.headers.get('endDate'))
            start_date = convert_timestamp_to_date(start_date_timestamp)
            end_date = convert_timestamp_to_date(end_date_timestamp)
            currency = request.headers.get('currency')

            times_queryset = get_time_entry_by_user_and_interval_date(user=user, start_date=start_date,
                                                                      end_date=end_date)
            rates_list = get_rate_by_user_and_interval_date_with_need_currency(user=user, start_date=start_date,
                                                                               end_date=end_date, currency=currency)

            avg_rate = get_current_avg_worker_rate_by_user_with_need_currency(user=user, currency=currency)

            work_time = WorkTimeSerializerForStatistics(user, context={'times_queryset': times_queryset}).data
            rate = RateSerializerForStatistics(user, context={'rates_list': rates_list}).data

            chart_points_count = int(request.headers.get('chartPointsCount'))

            context_for_salary = {
                "min_work_time": work_time['min'],
                "max_work_time": work_time['max'],
                "avg_work_time": work_time['average'],
                "total_work_time": work_time['total'],
                "avg_rate": avg_rate,
            }

            salary = SalarySerializerForStatistics(user, context=context_for_salary).data

            entries = get_entries_to_salary_chart(rate=avg_rate, times_queryset=times_queryset,
                                                  count_points=chart_points_count)

            if len(entries) == 0:
                entries.append(
                    {
                        'x': start_date_timestamp,
                        'y': 0
                    })
                entries.append(
                    {
                        'x': end_date_timestamp,
                        'y': 0
                    },
                )

            if len(entries) == 1:
                if convert_timestamp_to_date(entries[0]['x']) == convert_timestamp_to_date(start_date_timestamp):
                    entries.append(
                        {
                            'x': end_date_timestamp,
                            'y': 0
                        }
                    )
                elif convert_timestamp_to_date(entries[0]['x']) == convert_timestamp_to_date(end_date_timestamp):
                    entries.append(
                        {
                            'x': start_date_timestamp,
                            'y': 0
                        })
                else:
                    entries.append(
                        {
                            'x': start_date_timestamp,
                            'y': 0
                        })
                    entries.append(
                        {
                            'x': end_date_timestamp,
                            'y': 0
                        },
                    )

            import operator
            entries = sorted(entries, key=operator.itemgetter('x'))
            salary['chartDataSet'] = {'entries': entries}

            output_data = {
                'workTime': work_time,
                'rate': rate,
                'salary': salary
            }
            return Response(output_data, status=status.HTTP_200_OK)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)
