from main.models import ProjectEmployee, HistoryAdvance


def get_advances_by_worker(employee: ProjectEmployee):
    return HistoryAdvance.objects.filter(employee=employee)
