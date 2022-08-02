from main.models import Role, ProjectEmployee


def get_role_by_id(role_id: int):
    return Role.objects.filter(id=role_id).first()


def get_all_project_roles():
    return Role.objects.exclude(project=None)

