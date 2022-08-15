from main.models import AuthData, AppUser


def get_auth_data_by_refresh_token(refresh):
    return AuthData.objects.filter(refresh_token_data=refresh).first()


def get_tokens_by_user(user: AppUser):
    return AuthData.objects.filter(user=user)
