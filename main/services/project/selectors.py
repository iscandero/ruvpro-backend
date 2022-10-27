from main.models import AppUser, Project, ProjectEmployee


def get_projects_for_owner_or_member(viewer_user: AppUser, archived=None):
    projects_ids = ProjectEmployee.objects.filter(user=viewer_user).values_list('project', flat=True)

    if archived == 'false':
        is_archived = False
    elif archived == 'true':
        is_archived = True

    if archived is not None:
        return Project.objects.filter(owner=viewer_user, is_archived=is_archived) | Project.objects.exclude(
            owner=viewer_user).filter(
            id__in=projects_ids, is_archived=is_archived)

    return Project.objects.filter(owner=viewer_user) | Project.objects.exclude(
        owner=viewer_user).filter(id__in=projects_ids)


def get_projects_ids_by_owner(owner_project: AppUser):
    return list(Project.objects.filter(owner=owner_project).values_list('id', flat=True))


def get_projects_ids_by_owner_or_member(owner_or_member_project: AppUser):
    projects_ids = list(
        ProjectEmployee.objects.filter(user=owner_or_member_project).values_list('project_id', flat=True)) + \
                   list(Project.objects.filter(owner=owner_or_member_project).values_list('id', flat=True))
    return projects_ids


def get_project_by_id(project_id: int):
    return Project.objects.get(id=project_id)


def get_all_project_ids_list_by_owner_projects(owner_projects: AppUser) -> list:
    return list(Project.objects.filter(owner=owner_projects).values_list('id', flat=True))


def get_all_project():
    return Project.objects.all()
