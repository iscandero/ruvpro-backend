from main.models import Project
from main.services.role.project_role.interactos import get_amount_intern_role_in_project
from main.services.role.project_role.selectors import get_role_by_project_and_name
from main.services.worker.selectors import get_workers_by_project_and_role
from main.models import ProjectEmployee


def get_income_all_interns_in_project(project: Project):
    intern_role = get_role_by_project_and_name(project=project, role_name='Испытательный срок')
    amount_intern_role = get_amount_intern_role_in_project(project=project)
    interns_in_project = get_workers_by_project_and_role(project=project, role=intern_role)
    count_interns = interns_in_project.count()
    return amount_intern_role * count_interns


def calculate_master_or_mentor_salary(worker: ProjectEmployee):
    """
    Подсчёт зп работника с ролью-Мастер или Ментор
    """
    project = worker.project
    worker_time = worker.work_time
    average_rate = project.average_rate
    interns_amount = get_income_all_interns_in_project(project=project)
    coefficient_from_assist = (100 - get_role_by_project_and_name(project=project,
                                                                  role_name='Подсобный').percentage) / 100

    coefficient_from_pupil = (100 - get_role_by_project_and_name(project=project,
                                                                 role_name='Ученик').percentage) / 100

    share_from_assist = coefficient_from_assist * average_rate * project.assists_work_time

    share_from_intern = average_rate * project.interns_work_time - interns_amount

    if worker.role.name == 'Мастер':
        share_from_pupil = coefficient_from_pupil * average_rate * project.pupils_work_time
    else:
        share_from_pupil = 1.1 * coefficient_from_pupil * average_rate * project.pupils_work_time

    masters_and_mentors_times = project.masters_work_time + project.mentors_work_time
    masters_and_mentors_times_for_pupil_share = project.masters_work_time + 1.1 * project.mentors_work_time

    if masters_and_mentors_times is not None and masters_and_mentors_times != 0:
        part_1 = (share_from_assist + share_from_intern) / masters_and_mentors_times
        part_2 = share_from_pupil / masters_and_mentors_times_for_pupil_share
        salary = worker_time * (average_rate + part_1 + part_2)
    else:
        salary = 0

    return salary


def calculate_standard_salary(worker: ProjectEmployee):
    """
    Подсчёт зп работника
    который не получает доп.плату за других сотрудников проекта
    """
    role_percentage = worker.role.percentage
    worker_time = worker.work_time
    average_rate = worker.project.average_rate

    salary = worker_time * average_rate * (role_percentage / 100)

    return salary
