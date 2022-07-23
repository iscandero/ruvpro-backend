from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from main.models import TimeEntry, ProjectEmployee
from main.services.project.use_cases import get_budget_without_additional_income_in_project, \
    update_roles_time_in_project_by_worker, subtract_work_time_from_project_by_worker
from main.services.time_entry.use_cases import get_sum_work_time_by_workers, get_sum_work_time_by_worker
from main.services.worker.selectors import get_ids_workers_by_project


@receiver(post_save, sender=TimeEntry)
def calculate_project_work_time_and_avg_rate(sender, instance, **kwargs):
    project = instance.employee.project
    workers_in_this_project = get_ids_workers_by_project(project=project)

    time_aggregate = get_sum_work_time_by_workers(workers=workers_in_this_project)

    project_work_time = time_aggregate if time_aggregate is not None else 0

    project.work_time = project_work_time

    budget_without_additional_income = get_budget_without_additional_income_in_project(project=project)
    project.average_rate = budget_without_additional_income / project_work_time if project_work_time != 0 else 0
    project.save(update_fields=['work_time'])
    project.save(update_fields=['average_rate'])


@receiver(post_save, sender=TimeEntry)
def calculate_worker_work_time(sender, instance, **kwargs):
    worker = instance.employee
    time_aggregate = get_sum_work_time_by_worker(worker=worker)
    worker.work_time = time_aggregate if time_aggregate is not None else 0
    worker.save(update_fields=['work_time'])


@receiver(post_save, sender=TimeEntry)
def calculate_roles_workers_work_time_in_project(sender, instance, **kwargs):
    worker = instance.employee
    update_roles_time_in_project_by_worker(worker=worker)


@receiver(pre_delete, sender=ProjectEmployee)
def calculate_project_time_data_from_delete_worker(sender, instance, **kwargs):
    project = instance.project

    subtract_work_time_from_project_by_worker(worker=instance, work_time_for_sub=instance.work_time)

    project_work_time = project.work_time

    budget_without_additional_income = get_budget_without_additional_income_in_project(project=project)

    project.average_rate = budget_without_additional_income / project_work_time if project_work_time != 0 else 0
    project.save(update_fields=['average_rate'])
