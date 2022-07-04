from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from main.signals.role_signals import create_or_delete_base_roles
        from main.signals.advance_signals import write_advance_to_history_model
        from main.signals.time_entry_signals import calculate_project_work_time, calculate_worker_work_time
