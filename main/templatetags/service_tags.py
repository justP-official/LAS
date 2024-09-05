from django import template

register = template.Library()

@register.inclusion_tag('main/templatetags_templates/form.html')
def draw_form(form):
    """
    Шаблонный тег для отрисовки форм.
    
    Параметры:
    ----------
    form - Экземпляр формы, которую необходимо рендерить в html-разметку.

    Возвращаемое значение:
    ----------------------
    context - Словарь с контекстными переменными
    """
    context = {'form': form}
    return context
