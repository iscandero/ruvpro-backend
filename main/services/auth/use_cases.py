from main.models import AppUser, AuthData
from main.services.auth.selectors import get_tokens_by_user


def delete_all_tokens_by_user(user: AppUser):
    get_tokens_by_user(user=user).delete()
