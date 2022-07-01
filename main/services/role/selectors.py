from main.models import Role


def get_role_by_id(role_id: int):
    return Role.objects.filter(id=role_id).first()
