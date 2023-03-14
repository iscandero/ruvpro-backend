import random
import string
from datetime import datetime
from operator import itemgetter

from main.const_data.serv_info import SERV_NAME
from main.serializers.history_serializers import AdvanceTimeEntrySerializerForHistory
from main.services.history.interactors import get_chain_advance_time_entry_queryset, \
    get_chain_advance_time_entry_queryset_by_workers
from main.services.project.selectors import get_project_by_id
from main.services.report.interactors import create_pdf_report, create_report_object
from main.services.work_with_date import convert_timestamp_to_date
from main.services.worker.selectors import get_all_workers_by_project_id


def create_user_current_project_report(user, project_id=None, from_date=None, to_date=None):
    """
    user - объект модели AppUser
    project_id - int, id проекта, по которому создаётся отчёт
    from_date, to_date - необходимый интервал дат


    Если передан id проекта, создаёт отчёт для заданного пользователя на заданном проекте
    Если id проекта не указан, создаёт отчёт для заданного пользователя на всех проектах, где он работает
    """

    queryset = get_chain_advance_time_entry_queryset(user, project_id, from_date, to_date)
    serializer = AdvanceTimeEntrySerializerForHistory(queryset, many=True)
    serialized_data = serializer.data

    flag_interval = False
    if from_date and to_date:
        from_date = convert_timestamp_to_date(float(from_date)).strftime('%d.%m.%Y')
        to_date = convert_timestamp_to_date(float(to_date)).strftime('%d.%m.%Y')
        flag_interval = True

    data = []
    if project_id:
        if flag_interval:
            report_name = f'{get_project_by_id(project_id).name.replace(" ", "_")} {user.name} с {from_date} по {to_date}'
        else:
            report_name = f'{get_project_by_id(project_id).name.replace(" ", "_")} {user.name} {datetime.now().date()}'

        titles_list = ['Дата', 'Рабочие часы', 'Аванс', 'Заработная плата', 'Валюта']

        for row in serialized_data:
            date = str(convert_timestamp_to_date(row['date']))
            work_time = row['workTime'] if row['workTime'] else 0
            advance = row['advance'] if row['advance'] else 0
            salary = round(row['salary'], 4) if row['salary'] else 0
            data.append([date, str(work_time), str(advance), str(salary), str(row['currency'])])
    else:
        if flag_interval:
            report_name = f'{user.name} с {from_date} по {to_date}'
        else:
            report_name = f'{user.name} {datetime.now().date()}'

        titles_list = ['Дата', 'Рабочие часы', 'Аванс', 'Заработная плата', 'Валюта', 'Проект']
        for row in serialized_data:
            date = str(convert_timestamp_to_date(row['date']))
            work_time = row['workTime'] if row['workTime'] else 0
            advance = row['advance'] if row['advance'] else 0
            salary = round(row['salary'], 4) if row['salary'] else 0
            project = get_project_by_id(row['projectId']).name
            data.append([date, str(work_time), str(advance), str(salary), str(row['currency']), str(project)])

        data = sorted(data, key=itemgetter(5))

    file_name = ''.join(random.choice(string.ascii_lowercase) for i in range(24))
    create_pdf_report(titles_list=titles_list, data_list=data, report_name=file_name)
    return create_report_object(user=user, date=datetime.now().date(),
                                url=SERV_NAME + '/media' + '/users_reports' + '/' + file_name + '.pdf',
                                name=report_name)


def create_current_project_report_for_all_workers(user, project_id, from_date=None, to_date=None):
    """
    user - объект модели AppUser (создателя проекта)
    project_id - int, id проекта, по которому создаётся отчёт
    from_date, to_date - необходимый интервал дат

    """

    workers = get_all_workers_by_project_id(project_id)
    queryset = get_chain_advance_time_entry_queryset_by_workers(workers, from_date, to_date)
    serializer = AdvanceTimeEntrySerializerForHistory(queryset, many=True)
    serialized_data = serializer.data

    flag_interval = False
    if from_date and to_date:
        from_date = convert_timestamp_to_date(float(from_date)).strftime('%d.%m.%Y')
        to_date = convert_timestamp_to_date(float(to_date)).strftime('%d.%m.%Y')
        flag_interval = True

    if flag_interval:
        report_name = f'{get_project_by_id(project_id).name.replace(" ", "_")} с {from_date} по {to_date}'
    else:
        report_name = f'{get_project_by_id(project_id).name.replace(" ", "_")} {datetime.now().date()}'

    titles_list = ['Дата', 'Рабочие часы', 'Аванс', 'Заработная плата', 'Валюта', 'Имя']

    data = []
    for row in serialized_data:
        date = str(convert_timestamp_to_date(row['date']))
        work_time = row['workTime'] if row['workTime'] else 0
        advance = row['advance'] if row['advance'] else 0
        salary = round(row['salary'], 4) if row['salary'] else 0
        name = str(row['name'])

        data.append([date, str(work_time), str(advance), str(salary), str(row['currency']), str(name)])

    data = sorted(data, key=itemgetter(5))

    file_name = ''.join(random.choice(string.ascii_lowercase) for i in range(24))
    create_pdf_report(titles_list=titles_list, data_list=data, report_name=file_name)
    return create_report_object(user=user, date=datetime.now().date(),
                                url=SERV_NAME + '/media' + '/users_reports' + '/' + file_name + '.pdf',
                                name=report_name)
