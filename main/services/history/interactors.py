import operator
from itertools import chain

from main.services.advance.selectors import get_advances_by_user_and_project_id, get_advances_by_user, \
    get_advances_by_workers
from main.services.time_entry.selectors import get_time_entrys_by_user_and_project_id, get_time_entrys_by_user, \
    get_time_entrys_by_workers
from main.services.work_with_date import convert_timestamp_to_date


def get_chain_advance_time_entry_queryset(user, project_id=None, from_date=None, to_date=None):
    if from_date and to_date:
        from_date = convert_timestamp_to_date(float(from_date))
        to_date = convert_timestamp_to_date(float(to_date))

    if project_id:
        if from_date and to_date:
            time_entrys = get_time_entrys_by_user_and_project_id(user, project_id).filter(date__gte=from_date,
                                                                                          date__lte=to_date)
            dates_list = time_entrys.values_list('date', flat=True)
            advances = get_advances_by_user_and_project_id(user, project_id).filter(date__gte=from_date,
                                                                                    date__lte=to_date).exclude(
                date__in=dates_list)
        else:
            time_entrys = get_time_entrys_by_user_and_project_id(user, project_id)
            dates_list = time_entrys.values_list('date', flat=True)
            advances = get_advances_by_user_and_project_id(user, project_id).exclude(date__in=dates_list)

        no_sorted_queryset = list(chain(time_entrys, advances))
        queryset = sorted(no_sorted_queryset, key=operator.attrgetter('date'), reverse=True)
    else:
        if from_date and to_date:
            time_entrys = get_time_entrys_by_user(user).filter(date__gte=from_date, date__lte=to_date)
            dates_list = time_entrys.values_list('date', flat=True)
            advances = get_advances_by_user(user).filter(date__gte=from_date, date__lte=to_date).exclude(
                date__in=dates_list)
        else:
            time_entrys = get_time_entrys_by_user(user)
            dates_list = time_entrys.values_list('date', flat=True)
            advances = get_advances_by_user(user).exclude(date__in=dates_list)
        no_sorted_queryset = list(chain(time_entrys, advances))
        queryset = sorted(no_sorted_queryset, key=operator.attrgetter('date'), reverse=True)

    return queryset


def get_chain_advance_time_entry_queryset_by_workers(workers, from_date=None, to_date=None):
    if from_date and to_date:
        from_date = convert_timestamp_to_date(float(from_date))
        to_date = convert_timestamp_to_date(float(to_date))

        time_entrys = get_time_entrys_by_workers(workers).filter(date__gte=from_date, date__lte=to_date)
        dates_list = time_entrys.values_list('date', flat=True)
        advances = get_advances_by_workers(workers).exclude(date__in=dates_list).filter(date__gte=from_date,
                                                                                        date__lte=to_date)

    else:
        time_entrys = get_time_entrys_by_workers(workers)
        dates_list = time_entrys.values_list('date', flat=True)
        advances = get_advances_by_workers(workers).exclude(date__in=dates_list)

    no_sorted_queryset = list(chain(time_entrys, advances))
    queryset = sorted(no_sorted_queryset, key=operator.attrgetter('date'), reverse=True)
    return queryset
