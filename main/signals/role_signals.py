from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import AppUser
from main.services.role.base_role.use_cases import create_base_roles_if_needed


@receiver(post_save, sender=AppUser)
def create_base_roles(sender, instance, created, update_fields, **kwargs):
    create_base_roles_if_needed(instance)



