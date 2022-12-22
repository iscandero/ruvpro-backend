from main.services.role.project_role.selectors import get_role_by_project_and_name

from main.services.time_entry.interactors import calculate_work_time_all_workers_with_role


def get_budget_without_additional_income_in_project(project):
    amortization_role = get_role_by_project_and_name(project=project, role_name='Амортизация инструмента')
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
