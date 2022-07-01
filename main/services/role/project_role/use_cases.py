from main.models import AppUser, Project
from main.services.role.base_role.selectors import get_all_base_roles_by_author


def create_project_roles_for_owner_new_project(project_owner: AppUser, new_project: Project) -> None:
    """
    Создание проектых ролей для пользователя,
    который создал проект
    """
    base_roles = get_all_base_roles_by_author(author=project_owner)
    if base_roles is not None:
        for base_role in base_roles:
            base_role.id = None
            base_role.project = new_project
            base_role.is_base = False
            base_role.save()
