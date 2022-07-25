from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import HistoryAdvance
from main.services.advance.use_cases import get_sum_advance_by_worker


@receiver(post_save, sender=HistoryAdvance)
def calculate_worker_work_time(sender, instance, **kwargs):
    worker = instance.employee
    advance_aggregate = get_sum_advance_by_worker(worker=worker)
    worker.advance = advance_aggregate if advance_aggregate is not None else 0
    worker.save(update_fields=['work_time'])
