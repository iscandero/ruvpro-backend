from main.models import TimeEntry, ProjectEmployee


def get_time_entry_employees_by_ids_list(employees: list):
    return TimeEntry.objects.filter(employee_id__in=employees)


def get_time_entry_employees_by_project(employee: ProjectEmployee):
    return TimeEntry.objects.filter(employee=employee)
