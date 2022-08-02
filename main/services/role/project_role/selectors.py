from django.contrib.auth.models import User

from main.models import AppUser, Project, Role, ProjectEmployee


def get_role_by_name_and_author_and_project(name: str, author: AppUser, project: Project):
    return Role.objects.filter(name=name, author_id=author, project=project).first()


def is_user_has_role_in_project(user: User, role: Role, project: Project) -> bool:
    return True if ProjectEmployee.objects.filter(project=project, user=user,
                                                  role=role) else False


def get_role_by_project_and_name(project: Project, role_name: str):
    return Role.objects.filter(is_base=False, project=project, name=role_name).first()


def get_roles_by_project(project: Project):
    return Role.objects.filter(project=project)


def get_role_by_name_and_project(name: str, project: Project):
    return Role.objects.filter(name=name, project=project).get()