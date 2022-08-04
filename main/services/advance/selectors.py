from main.models import ProjectEmployee, HistoryAdvance
from main.services.project.selectors import get_project_by_id
from main.services.worker.selectors import get_worker_by_id, get_workers_by_project


def get_advances_by_worker(employee: ProjectEmployee):
    return HistoryAdvance.objects.filter(employee=employee)


def get_advance_by_date_and_worker(worker: ProjectEmployee, date):
    return HistoryAdvance.objects.filter(employee=worker, date=date).first()


def get_advance_by_date_and_worker_id(worker_id: int, date):
    advance = HistoryAdvance.objects.filter(employee_id=worker_id, date=date).first()
    if advance:
        return advance

    worker = get_worker_by_id(worker_id=worker_id)
    return HistoryAdvance.objects.create(date=date, employee=worker, advance=0)


def get_advance_by_date_and_project_id(project_id: int, date):
    project = get_project_by_id(project_id=project_id)
    worker_ids = get_workers_by_project(project=project).values_list('id', flat=True)
    advances = []
    for worker_id in worker_ids:
        advances.append(get_advance_by_date_and_worker_id(worker_id=worker_id, date=date))

    return advances
