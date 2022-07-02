from main.const_data.serv_info import SERV_NAME
from main.models import AppUser, ProjectEmployee


def is_sub_user(user: AppUser) -> bool:
    return True if user.authority == 1 else False


def get_app_user_by_token(token: str):
    return AppUser.objects.filter(token_data=token).first()


def is_exist_user_phone(phone: str):
    return True if AppUser.objects.filter(phone=phone) else False


def get_app_user_by_id(id: int):
    return AppUser.objects.filter(id=id).first()


def get_app_user_by_worker(worker: ProjectEmployee):
    return worker.user


def get_avatar_path(user: AppUser):
    return None if not user.avatar else SERV_NAME + str(user.avatar.url)
