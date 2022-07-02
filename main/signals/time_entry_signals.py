from django.db.models import Sum
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from main.models import TimeEntry
from main.services.time_entry.selectors import get_time_entry_employees_by_ids_list, get_time_entry_employees_by_project
from main.services.worker.selectors import get_ids_workers_by_project


@receiver([post_save, post_delete], sender=TimeEntry)
def calculate_project_work_time(sender, instance, **kwargs):
    project = instance.employee.project
    workers_in_this_project = get_ids_workers_by_project(project=project)
    time_aggregate = get_time_entry_employees_by_ids_list(employees=workers_in_this_project).aggregate(
        sum_time=Sum('work_time'))
    project.work_time = time_aggregate['sum_time'] if time_aggregate['sum_time'] is not None else 0
    project.save(update_fields=['work_time'])


@receiver([post_save, post_delete], sender=TimeEntry)
def calculate_worker_work_time(sender, instance, **kwargs):
    worker = instance.employee
    time_aggregate = get_time_entry_employees_by_project(employee=worker).aggregate(sum_time=Sum('work_time'))
    worker.work_time = time_aggregate['sum_time'] if time_aggregate['sum_time'] is not None else 0
    worker.save(update_fields=['work_time'])
