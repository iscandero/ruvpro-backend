from main.models import ProjectEmployee, AppUser, Role, Project
from main.services.project.selectors import get_all_project_ids_list_by_owner_projects, \
    get_projects_ids_by_owner_or_member, get_all_projects_by_owner


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


def get_workers_by_user_ids_list_and_owner_projects(user_ids_list: list, owner_projects: AppUser) -> list:
    """
    Берёт все ID проектов, которые создал owner_projects
    Возвращает всех работников этих проектов,
    у которых id их user-ов находятся в user_ids_list
    """
    need_project_ids_list = get_all_project_ids_list_by_owner_projects(owner_projects=owner_projects)
    return list(
        ProjectEmployee.objects.filter(user_id__in=user_ids_list, project_id__in=need_project_ids_list).values_list(
            'id', flat=True))


def get_workers_by_user_and_willing(user: AppUser, willing: AppUser):
    """
    Возвращает доступыне для willing
    экземпляры модели ProjectEmployee с пользователем user
    """
    projects_ids = get_projects_ids_by_owner_or_member(owner_or_member_project=willing)
    return get_workers_by_user_and_projects_ids(user=user, projects_ids=projects_ids)


def get_all_workers():
    return ProjectEmployee.objects.all()


def get_worker_ids_by_user(user: AppUser):
    return ProjectEmployee.objects.filter(user=user).values_list('id', flat=True)


def get_workers_by_user(user: AppUser):
    return ProjectEmployee.objects.filter(user=user)


def get_worker_by_user_and_project_id(user: AppUser, project_id: int):
    return ProjectEmployee.objects.get(user=user, project_id=project_id)


def get_all_workers_by_project_id(project_id):
    return ProjectEmployee.objects.filter(project_id=project_id)
