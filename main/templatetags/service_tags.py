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

@register.inclusion_tag('main/templatetags_templates/pagination.html')
def pagination(page_obj, paginator):
    """
    Шаблонный тег для отрисовки пагинации.
    
    Параметры:
    ----------
    page_obj - Объект текущей страницы.
    paginator - Объект пагинатора. Хранит данные о количестве страниц.

    Возвращаемое значение:
    ----------------------
    context - Словарь с контекстными переменными
    """
    context = {
        'page_obj': page_obj, 
        'paginator': paginator
        }
    
    return context
