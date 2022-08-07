import datetime

from django.db.models import Sum, Min, Max, Avg


def sum_queryset(queryset, field):
    if queryset:
        queryset_aggregate = queryset.aggregate(sum=Sum(f'{field}'))
        return queryset_aggregate['sum']
    return 0


def min_queryset(queryset, field):
    if queryset:
        queryset_aggregate = queryset.aggregate(min=Min(f'{field}'))
        return queryset_aggregate['min']
    return 0


def max_queryset(queryset, field):
    if queryset:
        queryset_aggregate = queryset.aggregate(max=Max(f'{field}'))
        return queryset_aggregate['max']
    return 0


def avg_queryset(queryset, field):
    if queryset:
        queryset_aggregate = queryset.aggregate(avg=Avg(f'{field}'))
        return queryset_aggregate['avg']
    return 0


def get_entries_to_salary_chart(rate, times_queryset, count_points):
    if times_queryset:
        min_time_entry = min_queryset(queryset=times_queryset, field='work_time')
        max_time_entry = max_queryset(queryset=times_queryset, field='work_time')
        date_with_min_time_entry = times_queryset.filter(work_time=min_time_entry).first().date
        date_with_max_time_entry = times_queryset.filter(work_time=max_time_entry).last().date

        date_with_min_time_entry = datetime.datetime.combine(date_with_min_time_entry,
                                                             datetime.datetime.min.time()).timestamp()

        date_with_max_time_entry = datetime.datetime.combine(date_with_max_time_entry,
                                                             datetime.datetime.min.time()).timestamp()

        if date_with_max_time_entry != date_with_min_time_entry:
            entries = [{
                'x': date_with_min_time_entry,
                'y': rate * min_time_entry
            }, {
                'x': date_with_max_time_entry,
                'y': rate * max_time_entry
            }]

            if count_points != 2:
                first_date = datetime.datetime.combine(times_queryset.filter().first().date,
                                                       datetime.datetime.min.time()).timestamp()
                last_date = datetime.datetime.combine(times_queryset.filter().last().date,
                                                      datetime.datetime.min.time()).timestamp()
                interval = last_date - first_date
                count_points -= 2
                delta = interval / count_points

                times_queryset = times_queryset.exclude(work_time__in=[max_time_entry, min_time_entry])

                pre_value_timestamp = first_date
                for time_entry in times_queryset:
                    timestamp = datetime.datetime.combine(time_entry.date,
                                                          datetime.datetime.min.time()).timestamp()
                    if timestamp - pre_value_timestamp >= delta and len(entries) - 2 <= count_points:
                        entries.append({
                            'x': timestamp,
                            'y': rate * time_entry.work_time
                        })
                        pre_value_timestamp = timestamp
        else:
            entries = [{
                'x': date_with_max_time_entry,
                'y': rate * max_time_entry
            }]

        return entries

    return []
