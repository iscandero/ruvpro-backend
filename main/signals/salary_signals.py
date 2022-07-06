from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import Project, ProjectEmployee, Role
from main.services.salary.use_cases import calculate_worker_salary
from main.services.worker.selectors import get_workers_by_project, get_workers_by_project_role


@receiver(post_save, sender=Role)
def calculate_salary_if_change_role(sender, instance, update_fields, **kwargs):
    if update_fields == {'percentage'} or update_fields == {'amount'}:
        workers = get_workers_by_project_role(project_role=instance)
        for worker in workers:
            worker.salary = calculate_worker_salary(worker=worker)
            worker.save(update_fields=['salary'])


@receiver(post_save, sender=Project)
def calculate_salary_if_change_project(sender, instance, **kwargs):
    workers = get_workers_by_project(project=instance)
    if workers is not None:
        for worker in workers:
            worker.salary = calculate_worker_salary(worker=worker)
            worker.save(update_fields=['salary'])


@receiver(post_save, sender=ProjectEmployee)
def calculate_salary_if_change_project_employee(sender, instance, created, update_fields, **kwargs):
    if created or update_fields == {'role'}:
        project = instance.project
        workers = get_workers_by_project(project=project)
        if workers is not None:
            for worker in workers:
                worker.salary = calculate_worker_salary(worker=worker)
                worker.save(update_fields=['salary'])
