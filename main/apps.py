from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from main.signals.role_signals import create_or_delete_base_roles
        from main.signals.advance_signals import write_advance_to_history_model
        from main.signals.time_entry_signals import calculate_project_work_time_and_avg_rate, calculate_worker_work_time, \
            calculate_roles_workers_work_time_in_project
        from main.signals.salary_signals import calculate_salary_if_change_project, \
            calculate_salary_if_change_project_employee
