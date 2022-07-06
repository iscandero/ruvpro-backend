from django.db.models import Sum

from main.models import Project
from main.services.role.project_role.selectors import get_role_by_project_and_name
from main.services.worker.selectors import get_workers_by_project_and_role


def calculate_work_time_all_workers_with_role(project: Project, role_name: str) -> float:
    """
    Подсчёт рабочих часов всех сотрудников на проекте
    С ролью заданной по имени
    """

    need_project_role = get_role_by_project_and_name(project=project, role_name=role_name)
    need_workers = get_workers_by_project_and_role(project=project, role=need_project_role)
    sum_time = need_workers.aggregate(sum_wt=Sum('work_time'))
    return sum_time['sum_wt']
