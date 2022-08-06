from main.models import TimeEntry, ProjectEmployee
from main.services.project.selectors import get_project_by_id
from main.services.worker.selectors import get_worker_by_id, get_workers_by_project


def get_time_entry_employees_by_ids_list(employees: list):
    return TimeEntry.objects.filter(employee_id__in=employees)


def get_time_entrys_by_worker(employee: ProjectEmployee):
    return TimeEntry.objects.filter(employee=employee)


def get_time_entry_by_date_and_worker(worker: ProjectEmployee, date):
    return TimeEntry.objects.filter(date=date, employee=worker).first()


def get_time_entry_by_date_and_worker_id(worker_id: int, date):
    time_entry = TimeEntry.objects.filter(date=date, employee_id=worker_id).first()
    if time_entry:
        return time_entry

    worker = get_worker_by_id(worker_id=worker_id)
    return TimeEntry.objects.create(date=date, employee=worker, work_time=0)


def get_time_entry_by_date_and_project_id(project_id: int, date):
    project = get_project_by_id(project_id=project_id)
    worker_ids = get_workers_by_project(project=project).values_list('id', flat=True)
    times_entry = []
    for worker_id in worker_ids:
        times_entry.append(get_time_entry_by_date_and_worker_id(worker_id=worker_id, date=date))

    return times_entry
