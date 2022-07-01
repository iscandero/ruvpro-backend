from main.models import AppUser, Project


def get_projects_by_owner(owner_project: AppUser):
    return Project.objects.filter(owner_id=owner_project)


def get_project_by_id(project_id: int):
    return Project.objects.filter(id=project_id).first()
