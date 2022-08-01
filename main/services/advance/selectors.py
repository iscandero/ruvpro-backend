from main.models import ProjectEmployee, HistoryAdvance


def get_advances_by_worker(employee: ProjectEmployee):
    return HistoryAdvance.objects.filter(employee=employee)


def get_advance_by_date_and_worker(worker: ProjectEmployee, date):
    return HistoryAdvance.objects.filter(employee=worker, date=date).first()
