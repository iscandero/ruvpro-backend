from main.models import Project, ProjectTimeEntryHistory
from main.services.history_work_time_project.selectors import get_last_project_time_entry_history


def write_project_time_entry_to_history_table(project: Project):
    ProjectTimeEntryHistory.objects.create(project=project, work_time=project.work_time)


def get_last_project_time_in_history_model(project: Project):
    project_time_entry_history = get_last_project_time_entry_history(project=project)
    if project_time_entry_history is not None:
        return project_time_entry_history.work_time
    else:
        return -1


def calculate_difference_project_work_time(current_time, history_time):
    if history_time <= current_time and history_time != -1:
        return current_time - history_time
    else:
        return 0
