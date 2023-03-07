from fpdf import FPDF

from main.models import Report
from ruvpro.settings import STATIC_ROOT


def create_report_object(user, date, url):
    return Report.objects.create(user=user, date=date, url=url)


def create_pdf_report(titles_list: list, data_list: list, save_path: str):
    pdf = FPDF()
    pdf.add_font('DejaVu', '', STATIC_ROOT + '/DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 10)
    pdf.add_page()
    t = len(titles_list) + 0.5
    col_width = pdf.w / t
    row_height = pdf.font_size + 2
    data = [titles_list, *data_list]
    for row in data:
        for item in row:
            if item:
                item = item[:15]
            pdf.cell(col_width, row_height,
                     txt=item, border=1)
        pdf.ln(row_height)

    pdf.output(save_path)
