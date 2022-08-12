import datetime

from django.db.models import Sum, Min, Max, Avg

from main.services.work_with_date import convert_timestamp_to_date


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


def get_entries_to_work_time_chart(times_queryset, count_points):
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
                'y': min_time_entry
            }, {
                'x': date_with_max_time_entry,
                'y': max_time_entry
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
                    if timestamp - pre_value_timestamp >= delta:
                        entries.append({
                            'x': timestamp,
                            'y': time_entry.work_time
                        })
                        pre_value_timestamp = timestamp
        else:
            entries = [{
                'x': date_with_max_time_entry,
                'y': max_time_entry
            }]

        return entries

    return []


def get_normalize_entries_view(entries: list, start_date_timestamp, end_date_timestamp):
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

    return entries


def transform_work_time_entries_to_salary(entries: list, rate: float):
    new_entries = []
    for point in entries:
        new_point = point.copy()
        new_point['y'] *= rate
        new_entries.append(new_point)

    return new_entries


def transform_work_time_entries_to_seconds(entries: list):
    new_entries = []
    for point in entries:
        new_point = point.copy()
        new_point['y'] *= 3600
        new_entries.append(new_point)

    return new_entries
