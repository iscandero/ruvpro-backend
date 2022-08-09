from datetime import date

from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import ProjectEmployee, HistoryWorker, HistoryProject, Project


@receiver(post_save, sender=ProjectEmployee)
def write_to_history_worker(sender, instance, **kwargs):
    HistoryWorker.objects.create(date_change=date.today(), employee=instance,
                                 salary=instance.salary, rate=instance.project.average_rate,
                                 work_time=instance.work_time)


