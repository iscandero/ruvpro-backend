from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import Project, ProjectEmployee, Role, TimeEntry
from main.services.salary.use_cases import calculate_worker_salary
from main.services.worker.selectors import get_workers_by_project


@receiver(post_save, sender=TimeEntry)
@receiver(post_save, sender=Project)
@receiver(post_save, sender=Role)
@receiver(post_save, sender=ProjectEmployee)
def calculate_salary_signal(sender, created, instance, update_fields, **kwargs):
    if (sender == TimeEntry and (created or update_fields == {'work_time'})) or (
            sender == Project and update_fields == {'budget'}) or (sender == Role and instance.project is not None and (
            update_fields == {'percentage'} or update_fields == {'amount'})) or (
            sender == ProjectEmployee and update_fields == {'role'}):

        if sender == TimeEntry:
            project = instance.employee.project
        if sender == Project:
            project = instance
        if sender == Role or sender == ProjectEmployee:
            project = instance.project
        workers = get_workers_by_project(project=project)
        if workers is not None:
            for worker in workers:
                worker.salary = calculate_worker_salary(worker=worker)
                worker.save(update_fields=['salary'])
            # sum_salary_in_prj = workers.aggregate(sum_sal=Sum('salary'))
            # instance.sum_salary = sum_salary_in_prj['sum_sal']
            # instance.save(update_fields=['sum_salary'])
