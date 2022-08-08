from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from main.authentication import AppUserAuthentication
from main.const_data.template_errors import USER_NOT_FOUND_DATA, WORKER_NOT_FOUND
from main.serializers.statistics_serializers.personal_serializers import WorkTimeSerializerForStatistics, \
    SalarySerializerForStatistics
from main.serializers.statistics_serializers.projects_serializers import ProjectSerializerForStatistics, \
    ProjectSerializerForSpecificStatistics
from main.services.statistic.selectors import get_time_entry_by_worker_and_interval_date
from main.services.statistic.use_cases import get_entries_to_work_time_chart, transform_work_time_entries_to_seconds, \
    get_normalize_entries_view, transform_work_time_entries_to_salary
from main.services.work_with_date import convert_timestamp_to_date
from main.services.worker.selectors import get_workers_by_user, get_worker_by_user_and_project_id


class ProjectStatisticListAPIView(ListAPIView):
    authentication_classes = [AppUserAuthentication]
    serializer_class = ProjectSerializerForStatistics

    def list(self, request, *args, **kwargs):
        user = request.user
        if user:
            queryset = get_workers_by_user(user=user)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response({'projectsStatistics': serializer.data})

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)


class ProjectsStatisticAPIView(APIView):
    authentication_classes = [AppUserAuthentication]

    def get(self, request, pk):
        user = request.user
        if user:
            start_date_timestamp = float(request.headers.get('startDate'))
            end_date_timestamp = float(request.headers.get('endDate'))
            start_date = convert_timestamp_to_date(start_date_timestamp)
            end_date = convert_timestamp_to_date(end_date_timestamp)
            chart_points_count = int(request.headers.get('chartPointsCount'))

            try:
                worker = get_worker_by_user_and_project_id(user=user, project_id=pk)
            except:
                return Response(WORKER_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST)

            times_queryset = get_time_entry_by_worker_and_interval_date(worker=worker, start_date=start_date,
                                                                        end_date=end_date)

            work_time = WorkTimeSerializerForStatistics(user, context={'times_queryset': times_queryset}).data

            work_time_entries_hours = get_entries_to_work_time_chart(times_queryset=times_queryset,
                                                                     count_points=chart_points_count)

            normalize_entries = get_normalize_entries_view(entries=work_time_entries_hours,
                                                           start_date_timestamp=start_date_timestamp,
                                                           end_date_timestamp=end_date_timestamp)

            work_time_entries_seconds = transform_work_time_entries_to_seconds(normalize_entries)

            output_data = ProjectSerializerForSpecificStatistics(worker).data
            output_data['startDate'] = start_date_timestamp
            output_data['endDate'] = end_date_timestamp
            work_time['chartDataSet'] = {'entries': work_time_entries_seconds}
            output_data['workTimeStatistics'] = work_time

            worker_rate = worker.rate
            context_for_salary = {
                "min_work_time": work_time['min'],
                "max_work_time": work_time['max'],
                "avg_work_time": work_time['average'],
                "total_work_time": work_time['total'],
                "avg_rate": worker_rate,
            }

            salary = SalarySerializerForStatistics(user, context=context_for_salary).data
            salary_entries = transform_work_time_entries_to_salary(entries=normalize_entries, rate=worker_rate)
            salary['chartDataSet'] = {'entries': salary_entries}
            output_data['salaryStatistics'] = salary
            return Response(output_data, status=status.HTTP_200_OK)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)
