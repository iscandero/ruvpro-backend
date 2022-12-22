from main.services.currency.use_cases import convert_currency
from main.models import TimeEntry, AppUser, ProjectEmployee
from main.services.worker.selectors import get_worker_ids_by_user


def get_time_entry_by_user_and_interval_date(user: AppUser, start_date, end_date):
    """
    Возвращает TimeEntry работников с пользователем user
    в заданном интервале времени
    """
    workers_ids = get_worker_ids_by_user(user=user)
    return TimeEntry.objects.filter(date__gte=start_date, date__lte=end_date, employee_id__in=workers_ids).exclude(
        work_time=0)


def get_rates_list_by_user(user: AppUser, currency):
    """
    Возвращает текущие ставки работников с пользователем user
    конвертируя валюту в необходимую
    """
    workers_ids = get_worker_ids_by_user(user=user)
    workers_queryset = ProjectEmployee.objects.filter(id__in=workers_ids).exclude(rate=0)
    rates = []
    for worker in workers_queryset:
        project_currency = worker.project.currency
        if worker.rate != 0 and project_currency != currency:
            rates.append(convert_currency(amount=worker.rate, current_currency=project_currency,
                                          need_currency=currency))
        else:
            rates.append(worker.rate)

    return rates


def get_current_avg_worker_rate_by_user_with_need_currency(user: AppUser, currency):
    """
    Возвращает среднюю ставку по текущим ставкам
    работников с пользователем user в нужной валюте
    """
    workers = ProjectEmployee.objects.filter(user=user)
    rates = []
    for worker in workers:
        project_currency = worker.project.currency
        if worker.rate != 0 and project_currency != currency:
            rates.append(convert_currency(amount=worker.rate, current_currency=project_currency,
                                          need_currency=currency))
        else:
            rates.append(worker.rate)

    len_rates = len(rates)
    return sum(rates) / len_rates if len_rates != 0 else 0


def get_time_entry_by_worker_and_interval_date(worker: ProjectEmployee, start_date, end_date):
    """
    Возвращает TimeEntry работника worker
    в заданном интервале времени
    """
    return TimeEntry.objects.filter(date__gte=start_date, date__lte=end_date, employee=worker).exclude(
        work_time=0)
