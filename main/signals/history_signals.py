from datetime import date

from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import ProjectEmployee, HistoryAdvance, HistoryWorker, HistoryProject, Project


@receiver(post_save, sender=ProjectEmployee)
def write_to_history_advance(sender, instance, created, update_fields, **kwargs):
    if created or update_fields == {'advance'}:
        HistoryAdvance.objects.create(date_change=date.today(), employee=instance,
                                      advance=instance.advance)


@receiver(post_save, sender=ProjectEmployee)
def write_to_history_worker(sender, instance, created, update_fields, **kwargs):
    if created or 'salary' in update_fields or 'rate' in update_fields or 'work_time' in update_fields:
        HistoryWorker.objects.create(date_change=date.today(), employee=instance,
                                     salary=instance.salary, rate=instance.project.average_rate,
                                     work_time=instance.work_time)


# @receiver(post_save, sender=Project)
# def write_to_history_project(sender, instance, created, update_fields, **kwargs):
#     if created or 'salary' in update_fields or 'rate' in update_fields or 'work_time' in update_fields:
#         HistoryProject.objects.create(date_change=date.today(), employee=instance,
#                                      salary=instance.salary, rate=instance.project.average_rate,
#                                      work_time=instance.work_time)
