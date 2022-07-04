from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import HistoryAdvance, ProjectEmployee


@receiver(post_save, sender=ProjectEmployee)
def write_advance_to_history_model(sender, instance, created, update_fields, **kwargs):
    if created or update_fields == {'advance'}:
        if instance.advance is not None:
            HistoryAdvance.objects.create(advance=instance.advance, employee=instance)
