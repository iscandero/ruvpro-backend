from main.const_data.serv_info import SERV_NAME
from main.models import Project, ProjectEmployee
from main.services.user.selectors import get_avatar_path
from main.services.worker.selectors import get_workers_by_project


def get_rate_by_worker(worker: ProjectEmployee) -> float:
    if worker.project.average_rate is not None and worker.role.percentage is not None:
        rate = worker.project.average_rate * worker.role.percentage / 100
    elif worker.role.amount is not None and worker.work_time is not None and worker.work_time != 0:
        rate = worker.role.amount / worker.work_time
    else:
        rate = 0
    return rate

