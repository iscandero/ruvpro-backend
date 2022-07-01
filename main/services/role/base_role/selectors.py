from main.models import AppUser
from main.models import Role


def is_user_has_base_role_by_name(user: AppUser, name_role: str) -> bool:
    return Role.objects.filter(author_id=user, name=name_role, is_base=True)


def get_all_base_roles_by_author(author: AppUser):
    return Role.objects.filter(author_id=author, is_base=True)
