import io

from django.template.loader import render_to_string
from django.urls import reverse

from weasyprint import HTML, CSS

from PIL import Image, ImageDraw, ImageFont

from LAS import settings

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


def generate_png(report):
    """
    Функция для генерации png файла из отчёта.

    Параметры:
    ----------
    report - отчёт, содержащий информацию об уроках с конкретным учеником за определённый период.

    Возвращаемое значение:
    ----------------------
    img - готовое изображение.
    """

    lessons = get_lessons_for_period(report.pupil.id, report.start_period, report.end_period)

    img_weight = 600
    img_height = len(lessons) * 20 + 100

    x = 10
    y = 10
    dy = 20

    img = Image.new(size=(img_weight, img_height), color=(255, 255, 255), mode='RGB')

    drawer = ImageDraw.Draw(img)

    font = ImageFont.truetype(f"{settings.STATIC_ROOT}/assets/fonts/FreeSans.ttf", 16, encoding='UTF-8')

    drawer.text((x, y), f'{str(report)}:', fill=(0, 0, 0), font=font, align='center')

    y += dy

    for i, lesson in enumerate(lessons):
        lesson_text = f'{lesson.subject}; {lesson.lesson_datetime:%d %b %Y %H:%M}; '
        if lesson.lesson_duration != 1:
            lesson_text += f"Продолжительность урока: {format(lesson.lesson_duration, '.2f').rstrip('0').rstrip('.')} часа"

        drawer.text((x + 10, y), f'{i + 1}. {lesson_text}', fill=(0, 0, 0), font=font)
        y += dy

    y += dy

    drawer.line([(x, y), (img_weight - 10, y)], (0, 0, 0), 2)

    y += dy

    total_money = format(lessons.total_money(), '.2f').rstrip('0').rstrip('.')

    drawer.text((x, y), f'Итого: {total_money} руб', fill=(0, 0, 0), font=font)

    buff = io.BytesIO()

    img.save(buff, 'PNG')

    return buff.getvalue()
