from main.models import Project
from main.services.history_work_time_project.interactors import calculate_difference_project_work_time, \
    get_last_project_time_in_history_model


def get_difference_project_work_time(project: Project):
    current_time = project.work_time
    history_time = get_last_project_time_in_history_model(project=project)
    difference_time = calculate_difference_project_work_time(current_time=current_time, history_time=history_time)
    return difference_time * 3600
