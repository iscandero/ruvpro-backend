from main.models import Project, ProjectTimeEntryHistory


def get_last_project_time_entry_history(project: Project):
    return ProjectTimeEntryHistory.objects.filter(project=project).last()