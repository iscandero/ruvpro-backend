from django.db.models import Sum, Count

from main.models import ProjectEmployee
from main.services.time_entry.selectors import get_time_entry_employees_by_ids_list, get_time_entrys_by_worker, \
    get_not_zero_time_entry_by_worker


def get_sum_work_time_by_workers(workers):
    sum_wt = get_time_entry_employees_by_ids_list(employees=workers).aggregate(sum_time=Sum('work_time'))
    return sum_wt['sum_time']


def get_sum_work_time_by_worker(worker):
    time_aggregate = get_time_entrys_by_worker(employee=worker).aggregate(sum_time=Sum('work_time'))
    return time_aggregate['sum_time']


def get_count_workdays_by_worker(worker: ProjectEmployee):
    times_count = get_not_zero_time_entry_by_worker(worker=worker).aggregate(count=Count('id'))
    return times_count['count']
