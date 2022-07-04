from main.models import AppUser
from main.services.user.selectors import get_avatar_path


def get_app_user_output_data_with_social_list(user: AppUser, social_list: list) -> dict:
    avatar = get_avatar_path(user=user)

    data = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'phone': user.phone,
        'avatar': avatar,
        'bio': user.bio,
        'social': social_list,
        'authority': user.authority
    }

    return data


def get_short_user_output_data(user: AppUser):
    output_data = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
    }
    return output_data
