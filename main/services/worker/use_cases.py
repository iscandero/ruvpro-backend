from main.models import ProjectEmployee


def get_rate_by_worker(worker: ProjectEmployee) -> float:
    if worker.project.average_rate is not None and worker.work_time != 0:
        rate = worker.salary / worker.work_time
    elif worker.role.amount is not None and worker.work_time is not None and worker.work_time != 0:
        rate = worker.role.amount / worker.work_time
    else:
        rate = 0
    return rate
