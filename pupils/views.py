from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView
from django.views.generic.edit import CreateView, UpdateView

from pupils.models import Pupil

from pupils.forms import PupilsFilterForm, CreatePupilForm, UpdatePupilForm


class PupilsListView(LoginRequiredMixin, ListView):
    """Класс представления для страницы со списком учеников"""
    template_name = 'pupils/pupils_list.html'
    context_object_name = 'pupils'
    paginate_by = 5

    def get_queryset(self):
        pupils = Pupil.objects.filter(owner=self.request.user).prefetch_related('subjects')

        class_counter = self.request.GET.get('class_counter', None)

        skype_only = self.request.GET.get('skype_only', None)

        is_active = self.request.GET.get('is_active', None)

        subjects = self.request.GET.getlist('subjects', None)

        if class_counter:
            pupils = pupils.filter(class_counter=class_counter)

        if skype_only:
            pupils = pupils.filter(skype_only=skype_only)

        if is_active:
            pupils = pupils.filter(is_active=is_active)

        if subjects:
            print(subjects)
            pupils = pupils.filter(subjects__id__in=subjects)

        return pupils
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = PupilsFilterForm(data=self.request.GET) # сохраняет состояние формы при get-запросе
        context['title'] = 'L.A.S - Ученики'
        return context


class CreatePupilView(LoginRequiredMixin, CreateView):
    """Класс представления для страницы создания ученика"""
    template_name = 'pupils/create_pupil.html'
    form_class = CreatePupilForm
    success_url = reverse_lazy('pupils:pupils_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'L.A.S - Добавить ученика'
        return context
    
    def form_valid(self, form):
        form.instance.owner = self.request.user

        return super().form_valid(form)
    


class UpdatePupilView(LoginRequiredMixin, UpdateView):
    """Класс представления для страницы обновления данных ученика"""
    model = Pupil
    form_class = UpdatePupilForm
    template_name = 'pupils/update_pupil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'L.A.S - Обновить данные ученика'
        return context


class GetPupilPrice(LoginRequiredMixin, View):
    """Класс представления для получения цены за час урока"""
    def get_object(self, pupil_id, queryset=None):
        return Pupil.objects.get(id=pupil_id)
    
    def get(self, request, pupil_id):
        pupil = self.get_object(pupil_id)

        response_data = {'price_per_hour': pupil.price_per_hour}

        return JsonResponse(response_data)
