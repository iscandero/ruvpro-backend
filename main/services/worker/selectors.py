from main.models import ProjectEmployee, AppUser, Role, Project


def get_worker_by_user_role_project(user: AppUser, role: Role, project: Project):
    return ProjectEmployee.objects.filter(user=user, role=role, project=project).first()


def get_workers_by_project_role(project_role: Role):
    return ProjectEmployee.objects.filter(role=project_role)


def get_worker_by_id(worker_id: int):
    return ProjectEmployee.objects.filter(id=worker_id).first()


def get_workers_by_project(project: Project):
    return ProjectEmployee.objects.filter(project=project)


def get_ids_workers_by_project(project: Project):
    return get_workers_by_project(project=project).values_list('id', flat=True)


def get_workers_by_user_and_projects_ids(user: AppUser, projects_ids: list):
    return ProjectEmployee.objects.filter(user=user, project__id__in=projects_ids)


def get_workers_by_project_and_role(project: Project, role: Role):
    return ProjectEmployee.objects.filter(project=project, role=role)
