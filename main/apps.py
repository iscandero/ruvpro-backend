from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from main.signals.role_signals import create_or_delete_base_roles
        from main.signals.history_signals import write_to_history_advance, write_to_history_worker
        from main.signals.time_entry_and_rate_signals import calculate_project_work_time_and_avg_rate, \
            calculate_worker_work_time, \
            calculate_roles_workers_work_time_in_project, calculate_project_time_data_from_delete_worker
        from main.signals.salary_signals import calculate_salary_if_change_project, \
            calculate_salary_if_change_project_employee, calculate_salary_if_change_role
