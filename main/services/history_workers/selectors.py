from main.models import HistoryWorker


def get_workers_history_by_workers_ids_and_date_interval(workers_ids: list, start_date, end_date):
    return HistoryWorker.objects.filter(employee_id__in=workers_ids, date_change__gte=start_date,
                                        date_change__lte=end_date)
