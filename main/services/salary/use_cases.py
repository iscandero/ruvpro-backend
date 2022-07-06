from main.models import ProjectEmployee
from main.services.salary.interactors import calculate_master_or_mentor_salary, calculate_standard_salary


def calculate_worker_salary(worker: ProjectEmployee):
    if worker.role.name in ('Мастер', 'Ментор'):
        return calculate_master_or_mentor_salary(worker=worker)

    elif worker.role.name in ('Подсобный', 'Ученик'):
        return calculate_standard_salary(worker=worker)

    # Испытательный срок
    else:
        return worker.role.amount
