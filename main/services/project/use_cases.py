from main.models import Project, AppUser
from main.services.project.selectors import get_projects_by_owner, get_projects_ids_by_owner
from main.services.worker.selectors import get_workers_by_user_and_projects_ids


def get_full_output_project_data(project: Project, workers: list, roles: list) -> dict:
    output_data = {
        'id': project.id,
        'name': project.name,
        'workers': workers,
        'roles': roles,
        'budget': project.budget,
        'isArchived': project.is_archived,
        'workTime': project.work_time,
        'averageRate': project.average_rate,
    }
    return output_data


def get_short_output_projects_by_owner(owner: AppUser) -> list:
    projects = get_projects_by_owner(owner_project=owner)
    instance_output_list_of_dicts = []
    for project in projects:
        instance_output_list_of_dicts.append({'id': project.id,
                                              'name': project.name,
                                              'isArchived': project.is_archived,
                                              })
    return instance_output_list_of_dicts


def get_long_output_projects_by_owner(owner: AppUser) -> list:
    projects = get_projects_by_owner(owner_project=owner)
    instance_output_list_of_dicts = []
    for project in projects:
        instance_output_list_of_dicts.append({'id': project.id,
                                              'name': project.name,
                                              'budget': project.budget,
                                              'isArchived': project.is_archived,
                                              'workTime': project.work_time,
                                              'averageRate': project.average_rate
                                              })
    return instance_output_list_of_dicts


def get_output_projects_by_member_and_owner(member: AppUser, owner: AppUser) -> list:
    """
    Возвращает информацию о участнике member проекта
    c владельцем owner
    """
    projects_ids = get_projects_ids_by_owner(owner_project=owner)
    need_workers = get_workers_by_user_and_projects_ids(user=member, projects_ids=projects_ids)

    instance_output_data = []
    if need_workers:
        for need_worker in need_workers:
            instance_output_data.append(
                {
                    'id': need_worker.project.id,
                    'name': need_worker.project.name,
                    'role_id': need_worker.role.id,
                    'roleName': need_worker.role.name,
                    'roleColor': need_worker.role.color,
                }
            )
    return instance_output_data
