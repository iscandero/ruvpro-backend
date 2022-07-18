from main.const_data.serv_info import SERV_NAME
from main.models import Project, ProjectEmployee
from main.services.user.selectors import get_avatar_path
from main.services.worker.selectors import get_workers_by_project


def get_pretty_view_workers_by_project(project: Project) -> list:
    employees = get_workers_by_project(project=project)

    workers_output_list_of_dicts = []
    for worker in employees:
        avatar = None if not worker.user.avatar else SERV_NAME + str(worker.user.avatar.url)
        workers_output_list_of_dicts.append({'id': worker.id,
                                             'userId': worker.user_id,
                                             'rate': worker.project.average_rate,
                                             'advance': worker.advance,
                                             'roleId': worker.role_id,
                                             'roleName': worker.role.name,
                                             'roleColor': worker.role.color,
                                             'salary': 0,
                                             'work_time': 0,
                                             'avatar': avatar,
                                             'name': worker.user.name,
                                             'projectId': worker.project_id,
                                             })
    return workers_output_list_of_dicts


def get_worker_output_data(worker: ProjectEmployee):
    output_data = {
        'id': worker.id,
        'userId': worker.user.id,
        'rate': worker.project.average_rate,
        'advance': worker.advance,
        'roleId': worker.role.id,
        'salary': worker.salary,
        'workTime': worker.work_time,
        'name': worker.user.name,
        'projectId': worker.project.id,
        'roleName': worker.role.name,
        'roleColor': worker.role.color,
    }
    return output_data


def get_worker_output_data_for_statistic(worker: ProjectEmployee, income, work_time, rate):
    output_data = {
        'name': worker.user.name,
        'userId': worker.user.id,
        'income': income,
        'workTime': work_time,
        'rate': rate,
        'projectName': worker.project.name,
        'projectId': worker.project.id,
    }
    return output_data


def get_full_worker_output_data(worker: ProjectEmployee):
    avatar = get_avatar_path(user=worker.user)
    output_data = {
        'id': worker.id,
        'userId': worker.user.id,
        'rate': worker.project.average_rate,
        'advance': worker.advance,
        'roleId': worker.role.id,
        'salary': worker.salary,
        'workTime': worker.work_time,
        'avatar': avatar,
        'name': worker.user.name,
        'projectId': worker.project.id,
        'roleName': worker.role.name,
        'roleColor': worker.role.color,
    }
    return output_data
