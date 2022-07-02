from main.models import Project, AppUser
from main.services.project.selectors import get_projects_by_owner


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
                                              'name': project.name
                                              })
    return instance_output_list_of_dicts


def get_long_output_projects_by_owner(owner: AppUser) -> list:
    projects = get_projects_by_owner(owner_project=owner)
    instance_output_list_of_dicts = []
    for project in projects:
        instance_output_list_of_dicts.append({'id': project.id,
                                              'name': project.name,
                                              'budget': project.budget,
                                              'isArchived': project.id,
                                              'workTime': project.work_time,
                                              'averageRate': project.average_rate
                                              })
    return instance_output_list_of_dicts
