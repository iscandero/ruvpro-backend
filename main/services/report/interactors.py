import operator
import string
from datetime import datetime
import random
from itertools import chain

from fpdf import FPDF

from main.const_data.serv_info import SERV_NAME
from main.models import Report
from main.serializers.history_serializers import AdvanceTimeEntrySerializerForHistory
from main.services.advance.selectors import get_advances_by_user_and_project_id
from main.services.time_entry.selectors import get_time_entrys_by_user_and_project_id
from main.services.work_with_date import convert_timestamp_to_date
from ruvpro.settings import MEDIA_ROOT, STATIC_ROOT


def create_report_object_by_user_and_project(user, project_id):
    date = datetime.now().date()
    time_entrys = get_time_entrys_by_user_and_project_id(user, project_id)

    dates_list = time_entrys.values_list('date', flat=True)
    advances = get_advances_by_user_and_project_id(user, project_id).exclude(date__in=dates_list)
    no_sorted_queryset = list(chain(time_entrys, advances))
    queryset = sorted(no_sorted_queryset, key=operator.attrgetter('date'), reverse=True)
    serializer = AdvanceTimeEntrySerializerForHistory(queryset, many=True)
    serialized_data = serializer.data
    data = [['Дата', 'Рабочие часы', 'Аванс', 'Заработная плата', 'Валюта'], ]

    for row in serialized_data:
        date = str(convert_timestamp_to_date(row['date']))
        work_time = row['workTime'] if row['workTime'] else 0
        advance = row['advance'] if row['advance'] else 0
        salary = round(row['salary'], 4) if row['salary'] else 0
        data.append([date, str(work_time), str(advance), str(salary), str(row['currency'])])
    pdf = FPDF()
    pdf.add_font('DejaVu', '', STATIC_ROOT + '/DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 10)
    pdf.add_page()
    col_width = pdf.w / 6.5
    row_height = pdf.font_size + 2
    for row in data:
        for item in row:
            pdf.cell(col_width, row_height * 1,
                     txt=item, border=1)
        pdf.ln(row_height * 1)

    letters = string.ascii_lowercase
    rand_string = ''.join(random.choice(letters) for i in range(32))
    name = '/users_reports' + f'/{rand_string}.pdf'
    url = MEDIA_ROOT + name
    pdf.output(url)

    report = Report.objects.create(user=user, date=date, url=SERV_NAME + '/media' + name)

    return report
