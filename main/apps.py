from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from main.signals.role_signals import create_base_roles
        from main.signals.time_entry_and_rate_signals import calculate_project_and_worker_work_time, \
            calculate_project_avg_rate, calculate_project_time_data_from_delete_worker, calculate_worker_rate
        from main.signals.salary_signals import calculate_salary_signal
        from main.signals.advance_signals import calculate_worker_work_time
