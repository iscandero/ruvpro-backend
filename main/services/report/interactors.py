import jinja2
import pdfkit as pdfkit

from main.models import Report
from ruvpro.settings import STATIC_ROOT, MEDIA_ROOT


def create_report_object(user, date, url, name):
    return Report.objects.create(user=user, date=date, url=url, name=name)


def create_pdf_report(titles_list: list, data_list: list, report_name: str):
    template_loader = jinja2.FileSystemLoader(searchpath=STATIC_ROOT)
    template_env = jinja2.Environment(loader=template_loader)
    template_file = "report_template.html"
    template = template_env.get_template(template_file)
    output_data = template.render(titles_list=titles_list, data_list=data_list, report_name='Report')
    pdf_name = MEDIA_ROOT + '/users_reports' + '/' + report_name + '.pdf'
    pdfkit.from_string(str(output_data), pdf_name, options={"enable-local-file-access": ""})
