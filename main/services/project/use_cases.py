from main.models import Project, AppUser
from main.services.project.selectors import get_projects_by_owner, get_projects_ids_by_owner, \
    get_projects_ids_by_owner_or_member
from main.services.role.project_role.selectors import get_role_by_project_and_name
from main.services.role.use_cases import get_pretty_view_roles_by_project
from main.services.time_entry.interactors import calculate_work_time_all_workers_with_role
from main.services.worker.selectors import get_workers_by_user_and_projects_ids
from main.services.worker.use_cases import get_pretty_view_workers_by_project


def get_full_output_project_data(project: Project, workers: list, roles: list) -> dict:
    output_data = {
        'id': project.id,
        'name': project.name,
        'workers': workers,
        'roles': roles,
        'budget': project.budget,
        'isArchived': project.is_archived,
        'workTime': project.work_time * 3600,
        'averageRate': project.average_rate,
        'currency': project.currency,
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
                                              'workTime': project.work_time * 3600,
                                              'averageRate': project.average_rate,
                                              'currency': project.currency,
                                              })
    return instance_output_list_of_dicts


def get_long_output_projects_by_owner__full(owner: AppUser) -> list:
    projects = get_projects_by_owner(owner_project=owner)
    instance_output_list_of_dicts = []
    for project in projects:
        workers_output_list_of_dicts = get_pretty_view_workers_by_project(project=project)

        roles_output_list_of_dicts = get_pretty_view_roles_by_project(project=project)

        output_data = get_full_output_project_data(project=project, workers=workers_output_list_of_dicts,
                                                   roles=roles_output_list_of_dicts)
        instance_output_list_of_dicts.append(output_data)

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
                    'roleId': need_worker.role.id,
                    'roleName': need_worker.role.name,
                    'roleColor': need_worker.role.color,
                }
            )
    return instance_output_data


def get_output_projects_by_member_and_willing(member: AppUser, willing: AppUser) -> list:
    """
    Возвращает информацию о участнике member для желающего willing
    """
    projects_ids = get_projects_ids_by_owner_or_member(owner_or_member_project=willing)
    need_workers = get_workers_by_user_and_projects_ids(user=member, projects_ids=projects_ids)

    instance_output_data = []
    if need_workers:
        for need_worker in need_workers:
            instance_output_data.append(
                {
                    'id': need_worker.project.id,
                    'name': need_worker.project.name,
                    'roleId': need_worker.role.id,
                    'roleName': need_worker.role.name,
                    'roleColor': need_worker.role.color,
                }
            )
    return instance_output_data


def get_budget_without_additional_income_in_project(project):
    amortization_role = get_role_by_project_and_name(project=project, role_name='Аммортизация инструмента')
    amortization_inst_role_percentage = amortization_role.percentage if amortization_role is not None else 0

    journal_role = get_role_by_project_and_name(project=project, role_name='Журнал учета')
    journal_role_percentage = journal_role.percentage if journal_role is not None else 0

    resp_role = get_role_by_project_and_name(project=project, role_name='Ответственный за размеры и качество')
    resp_role_percentage = resp_role.percentage if resp_role is not None else 0

    percentage_for_deduction = 100 - amortization_inst_role_percentage - journal_role_percentage - resp_role_percentage

    return project.budget * percentage_for_deduction / 100


def update_roles_time_in_project_by_worker(worker):
    project = worker.project
    worker_role_name = worker.role.name

    if worker_role_name == 'Мастер':
        all_masters_work_time = calculate_work_time_all_workers_with_role(project=project, role_name='Мастер')
        project.masters_work_time = all_masters_work_time if all_masters_work_time is not None else 0
        project.save(update_fields=['masters_work_time'])

    if worker_role_name == 'Ментор':
        all_mentors_work_time = calculate_work_time_all_workers_with_role(project=project, role_name='Ментор')
        project.mentors_work_time = all_mentors_work_time if all_mentors_work_time is not None else 0
        project.save(update_fields=['mentors_work_time'])

    if worker_role_name == 'Подсобный':
        all_assists_work_time = calculate_work_time_all_workers_with_role(project=project, role_name='Подсобный')
        project.assists_work_time = all_assists_work_time if all_assists_work_time is not None else 0
        project.save(update_fields=['assists_work_time'])

    if worker_role_name == 'Ученик':
        all_pupils_work_time = calculate_work_time_all_workers_with_role(project=project, role_name='Ученик')
        project.pupils_work_time = all_pupils_work_time if all_pupils_work_time is not None else 0
        project.save(update_fields=['pupils_work_time'])

    if worker_role_name == 'Испытательный срок':
        all_interns_work_time = calculate_work_time_all_workers_with_role(project=project,
                                                                          role_name='Испытательный срок')
        project.interns_work_time = all_interns_work_time if all_interns_work_time is not None else 0
        project.save(update_fields=['interns_work_time'])


def subtract_work_time_from_project_by_worker(worker, work_time_for_sub):
    project = worker.project

    project.work_time -= work_time_for_sub
    project.save(update_fields=['work_time'])

    worker_role_name = worker.role.name
    if worker_role_name == 'Мастер':
        project.masters_work_time -= work_time_for_sub
        project.save(update_fields=['masters_work_time'])

    if worker_role_name == 'Ментор':
        project.mentors_work_time -= work_time_for_sub
        project.save(update_fields=['mentors_work_time'])

    if worker_role_name == 'Подсобный':
        project.assists_work_time -= work_time_for_sub
        project.save(update_fields=['assists_work_time'])

    if worker_role_name == 'Ученик':
        project.pupils_work_time -= work_time_for_sub
        project.save(update_fields=['pupils_work_time'])

    if worker_role_name == 'Испытательный срок':
        project.interns_work_time -= work_time_for_sub
        project.save(update_fields=['interns_work_time'])
