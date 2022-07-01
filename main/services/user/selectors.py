from main.models import AppUser


def is_sub_user(user: AppUser) -> bool:
    return True if user.authority == 1 else False
