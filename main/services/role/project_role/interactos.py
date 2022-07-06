from main.models import Project
from main.services.role.project_role.selectors import get_role_by_project_and_name


def get_amount_intern_role_in_project(project: Project):
    intern_role = get_role_by_project_and_name(project=project, role_name='Испытательный срок')
    return intern_role.amount


