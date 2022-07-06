from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from main.models import TimeEntry
from main.services.role.project_role.selectors import get_role_by_project_and_name
from main.services.time_entry.interactors import calculate_work_time_all_workers_with_role
from main.services.time_entry.selectors import get_time_entry_employees_by_ids_list, get_time_entry_employees_by_project
from main.services.worker.selectors import get_ids_workers_by_project


@receiver([post_save, post_delete], sender=TimeEntry)
def calculate_project_work_time_and_avg_rate(sender, instance, **kwargs):
    project = instance.employee.project
    workers_in_this_project = get_ids_workers_by_project(project=project)
    time_aggregate = get_time_entry_employees_by_ids_list(employees=workers_in_this_project).aggregate(
        sum_time=Sum('work_time'))
    project_work_time = time_aggregate['sum_time'] if time_aggregate['sum_time'] is not None else 0
    project.work_time = project_work_time
    amortization_inst_role_percentage = get_role_by_project_and_name(project=project,
                                                                     role_name='Аммортизация инструмента').percentage
    journal_role_percentage = get_role_by_project_and_name(project=project, role_name='Журнал учета').percentage

    percentage_for_deduction = 100 - amortization_inst_role_percentage - journal_role_percentage

    budget_without_additional_income = project.budget * percentage_for_deduction / 100
    project.average_rate = budget_without_additional_income / project_work_time if project_work_time != 0 else 0
    project.save(update_fields=['work_time', 'average_rate'])


@receiver([post_save, post_delete], sender=TimeEntry)
def calculate_worker_work_time(sender, instance, **kwargs):
    worker = instance.employee
    time_aggregate = get_time_entry_employees_by_project(employee=worker).aggregate(sum_time=Sum('work_time'))
    worker.work_time = time_aggregate['sum_time'] if time_aggregate['sum_time'] is not None else 0
    worker.save(update_fields=['work_time'])


@receiver([post_save, post_delete], sender=TimeEntry)
def calculate_roles_workers_work_time_in_project(sender, instance, **kwargs):
    worker = instance.employee
    project = instance.employee.project
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
