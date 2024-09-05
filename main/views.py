from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView

from user.forms import UserLoginForm


def view_404(request, exception):
    """Функция представления для обработки ошибки 404"""
    context = {'title': 'L.A.S - 404'}
    return render(request, '404.html', context)

def view_403(request, exception):
    """Функция представления для обработки ошибки 403"""
    context = {'title': 'L.A.S - 403'}
    return render(request, '403.html', context)

def view_500(request):
    """Функция представления для обработки ошибки 500"""
    context = {'title': 'L.A.S - 500'}
    return render(request, '500.html', context)


class IndexView(TemplateView):
    """Класс представления для отображения главной страницы"""
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserLoginForm()
        context['title'] = 'L.A.S - Главная'
        return context
