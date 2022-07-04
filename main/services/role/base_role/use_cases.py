from main.models import AppUser
from main.services.role.base_role.interactors import *
from main.services.role.base_role.selectors import get_all_base_roles_by_author


def create_base_roles_for_sub_user(roles_author: AppUser) -> None:
    """
    Создание базовых ролей для пользователя, который купил подписку
    Его authority = 1
    """
    add_master_role_if_needed(user=roles_author)
    add_mentor_role_if_needed(user=roles_author)
    add_auxiliary_role_if_needed(user=roles_author)
    add_student_role_if_needed(user=roles_author)
    add_acc_journal_role_if_needed(user=roles_author)
    add_amortization_instr_role_if_needed(user=roles_author)
    add_intern_role_if_needed(user=roles_author)


def delete_base_roles_for_unsub_user(roles_author: AppUser) -> None:
    """
    Удаление базовых ролей для пользователя, у которого закончилась подписка
    Его authority = 0
    """
    need_base_roles = get_all_base_roles_by_author(author=roles_author)

    if need_base_roles is not None:
        need_base_roles.delete()


def get_pretty_view_base_roles_by_user(user: AppUser) -> list:
    roles = get_all_base_roles_by_author(author=user)

    roles_output_list_of_dicts = []
    for role in roles:
        if role.percentage is not None:
            roles_output_list_of_dicts.append({
                'id': role.id,
                'name': role.name,
                'description': role.description,
                'color': role.color,
                'percentage': role.percentage,
                'type': role.type
            })
        else:
            roles_output_list_of_dicts.append({
                'id': role.id,
                'name': role.name,
                'description': role.description,
                'color': role.color,
                'amount': role.amount,
                'type': role.type
            })
    return roles_output_list_of_dicts
