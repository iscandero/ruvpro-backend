from main.models import Project, Role
from main.services.role.project_role.selectors import get_roles_by_project


def get_pretty_view_roles_by_project(project: Project) -> list:
    project_roles = get_roles_by_project(project=project)

    roles_output_list_of_dicts = []
    for role in project_roles:
        if role.percentage is not None:
            roles_output_list_of_dicts.append({
                'id': role.id,
                'name': role.name,
                'description': role.description,
                'color': role.color,
                'percentage': role.percentage,
                'type': role.type
            })
        else:
            roles_output_list_of_dicts.append({
                'id': role.id,
                'name': role.name,
                'description': role.description,
                'color': role.color,
                'amount': role.amount,
                'type': role.type
            })
    return roles_output_list_of_dicts


def get_role_output_data(role: Role) -> dict:
    if role.percentage is not None:
        output_data = {
            'id': role.id,
            'name': role.name,
            'description': role.description,
            'color': role.color,
            'percentage': role.percentage,
            'type': role.type
        }

    elif role.amount is not None:
        output_data = {
            'id': role.id,
            'name': role.name,
            'description': role.description,
            'color': role.color,
            'amount': role.amount,
            'type': role.type
        }

    else:
        output_data = {
            'id': role.id,
            'name': role.name,
            'description': role.description,
            'color': role.color,
            'amount': None,
            'type': role.type
        }

    return output_data
