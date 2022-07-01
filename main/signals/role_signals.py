from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import Project, AppUser
from main.services.role.base_role.use_cases import create_base_roles_for_sub_user, delete_base_roles_for_unsub_user


@receiver(post_save, sender=AppUser)
def create_or_delete_base_roles(sender, instance, created, update_fields, **kwargs):
    if (created or update_fields == {'authority'}) and instance.authority == 1:
        create_base_roles_for_sub_user(instance)

    if update_fields == {'authority'} and instance.authority == 0:
        delete_base_roles_for_unsub_user(roles_author=instance)


@receiver(post_save, sender=Project)
def post_save_signal_with_sender_project(sender, instance, created, update_fields, **kwargs):
    if created:
        ...
