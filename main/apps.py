from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from .signals.role_signals import create_or_delete_base_roles, post_save_signal_with_sender_project