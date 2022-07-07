from main.const_data.base_roles import *
from main.services.role.base_role.selectors import is_user_has_base_role_by_name
from main.services.user.selectors import is_sub_user
from main.models import AppUser, Role


def get_base_role_with_author(user: AppUser, base_role: dict) -> dict:
    """
    Склонировать шаблонную роль, хранящуюся словарём
    в объект Role, с указанием автора роли
    """
    base_role['author'] = user
    return base_role


def is_user_need_role_by_name(user: AppUser, name: str) -> bool:
    """
    Если пользователь имеет подписку и у него нет базовой роли
    с заданным названием -> пользователю нужна такая базовая роль
    """
    if is_sub_user(user=user):
        if not is_user_has_base_role_by_name(user=user, name_role=name):
            return True

    return False


def add_master_role_if_needed(user: AppUser) -> None:
    if is_user_need_role_by_name(user=user, name='Мастер'):
        role_to_create = get_base_role_with_author(user=user, base_role=MASTER_ROLE)
        Role.objects.create(**role_to_create)


def add_mentor_role_if_needed(user: AppUser) -> None:
    if is_user_need_role_by_name(user=user, name='Ментор'):
        role_to_create = get_base_role_with_author(user=user, base_role=MENTOR_ROLE)
        Role.objects.create(**role_to_create)


def add_auxiliary_role_if_needed(user: AppUser) -> None:
    if is_user_need_role_by_name(user=user, name='Подсобный'):
        role_to_create = get_base_role_with_author(user=user, base_role=AUXILIARY_ROLE)
        Role.objects.create(**role_to_create)


def add_student_role_if_needed(user: AppUser) -> None:
    if is_user_need_role_by_name(user=user, name='Ученик'):
        role_to_create = get_base_role_with_author(user=user, base_role=STUDENT_ROLE)
        Role.objects.create(**role_to_create)


def add_acc_journal_role_if_needed(user: AppUser) -> None:
    if is_user_need_role_by_name(user=user, name='Журнал учета'):
        role_to_create = get_base_role_with_author(user=user, base_role=ACC_JOURNAL_ROLE)
        Role.objects.create(**role_to_create)


def add_amortization_instr_role_if_needed(user: AppUser) -> None:
    if is_user_need_role_by_name(user=user, name='Аммортизация инструмента'):
        role_to_create = get_base_role_with_author(user=user, base_role=AMORTIZATION_INST_ROLE)
        Role.objects.create(**role_to_create)


def add_intern_role_if_needed(user: AppUser) -> None:
    if is_user_need_role_by_name(user=user, name='Испытательный срок'):
        role_to_create = get_base_role_with_author(user=user, base_role=INTERN_ROLE)
        Role.objects.create(**role_to_create)


def add_responsible_role_if_needed(user: AppUser) -> None:
    if is_user_need_role_by_name(user=user, name='Ответственный за размеры и качество'):
        role_to_create = get_base_role_with_author(user=user, base_role=RESPONSIBLE_ROLE)
        Role.objects.create(**role_to_create)
