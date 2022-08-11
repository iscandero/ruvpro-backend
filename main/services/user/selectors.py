from main.const_data.serv_info import SERV_NAME
from main.models import AppUser, ProjectEmployee, AuthData, FileUser


def is_sub_user(user: AppUser) -> bool:
    return True if user.authority == 1 else False


def get_app_user_by_token(token: str):
    auth_data = AuthData.objects.filter(token_data=token).first()
    if auth_data:
        return auth_data.user
    else:
        return auth_data


def is_exist_user_phone(phone: str):
    return True if AppUser.objects.filter(phone=phone).first() else False


def get_app_user_by_id(id: int):
    return AppUser.objects.filter(id=id).first()


def get_app_user_by_worker(worker: ProjectEmployee):
    return worker.user


def get_avatar_path(user: AppUser):
    return None if not user.avatar else SERV_NAME + str(user.avatar.url)


def get_app_user_by_email(email: str):
    return AppUser.objects.filter(email=email).first()


def get_app_user_by_phone(phone):
    return AppUser.objects.filter(email=phone).first()


def get_no_register_app_user_by_email(email: str):
    return AppUser.objects.filter(email=email, is_register=False).first()


def get_all_users():
    return AppUser.objects.all()


def get_all_files():
    return FileUser.objects.all()