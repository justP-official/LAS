from django.shortcuts import render
from django.views.generic import TemplateView

def view_404(request, exception):
    context = {'title': 'L.A.S - 404'}
    return render(request, '404.html', context)

def view_403(request, exception):
    context = {'title': 'L.A.S - 403'}
    return render(request, '403.html', context)

def view_500(request):
    context = {'title': 'L.A.S - 500'}
    return render(request, '500.html', context)


class IndexView(TemplateView):
    template_name = 'main/index.html'
    extra_context = {'title': 'L.A.S - Главная'}
