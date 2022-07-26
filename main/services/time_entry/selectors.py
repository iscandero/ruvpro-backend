from main.models import TimeEntry, ProjectEmployee


def get_time_entry_employees_by_ids_list(employees: list):
    return TimeEntry.objects.filter(employee_id__in=employees)


def get_time_entrys_by_worker(employee: ProjectEmployee):
    return TimeEntry.objects.filter(employee=employee)


def get_time_entry_by_date_and_worker(worker: ProjectEmployee, date):
    return TimeEntry.objects.filter(date=date, employee=worker).first()
