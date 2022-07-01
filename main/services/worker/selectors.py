from main.models import ProjectEmployee, AppUser, Role, Project


def get_worker_by_user_role_project(user: AppUser, role: Role, project: Project):
    return ProjectEmployee.objects.filter(user=user, role=role, project=project)


def get_worker_by_id(worker_id: int):
    return ProjectEmployee.objects.filter(id=worker_id).first()


def get_workers_by_project(project: Project):
    return ProjectEmployee.objects.filter(project=project)
