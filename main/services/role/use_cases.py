from main.models import Project
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
