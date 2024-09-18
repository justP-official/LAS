from django import template

from lessons.utils import get_lessons_for_period

register = template.Library()

@register.inclusion_tag('reports/templatetags_templates/report_lessons.html')
def report_lessons(pupil, start_period, end_period, report=None):
    """
    Шаблонный тег для отрисовки списка уроков с конкретным учеником за определённый период.
    
    Параметры:
    ----------
    pupil - Ученик, с которым были занятия за определённый период.

    start_period - начало периода.

    end_period - конец периода.

    Возвращаемое значение:
    ----------------------
    context - Словарь с контекстными переменными
    """
    context = {
        'lessons': get_lessons_for_period(pupil, start_period, end_period),
        'report': report
        }

    return context
