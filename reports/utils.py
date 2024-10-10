import requests

from django.template.loader import render_to_string
from django.urls import reverse

from weasyprint import HTML, CSS

import pymupdf

from lessons.utils import get_lessons_for_period


def generate_pdf(report, request):
    """
    Функция для генерации pdf файла из отчёта.

    Параметры:
    ----------
    report - отчёт, содержащий информацию об уроках с конкретным учеником за определённый период.

    request - запрос к серверу.

    Возвращаемое значение:
    ----------------------
    pdf - pdf файл
    """
    root_url = request.build_absolute_uri("/")

    lessons = get_lessons_for_period(report.pupil.id, report.start_period, report.end_period)

    html_string = render_to_string(
        "reports/templatetags_templates/report_lessons.html",
        context={"lessons": lessons, "report": report},
    )

    pdf = HTML(string=html_string, base_url=request.build_absolute_uri()).write_pdf(
        stylesheets=[
            CSS(base_url=request.build_absolute_uri(), url=f'{root_url}static/assets/css/bootstrap.min.css'),
            CSS(base_url=request.build_absolute_uri(), url=f'{root_url}static/assets/css/style.css'),
            CSS(string="body {background-color: #fff !important}")
            ]
    )

    return pdf


def convert_pdf_to_png(report, request):
    """
    Функция для генерации png файла из pdf.

    Параметры:
    ----------
    report - отчёт, содержащий информацию об уроках с конкретным учеником за определённый период.

    request - запрос к серверу.

    Возвращаемое значение:
    ----------------------
    png - png файл
    """
    root_url = request.build_absolute_uri("/")

    r = requests.get(f"{root_url}{reverse('reports:save_report_as_pdf', kwargs={'report_id': report.id})}").content

    doc = pymupdf.Document(stream=r)

    png = doc[0].get_pixmap().tobytes("png")

    return png
