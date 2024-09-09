import datetime

from django.utils import timezone
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from lessons.models import Lesson

from lessons.forms import LessonsFilterForm, CreateLessonForm, UpdateLessonForm


class LessonsListView(LoginRequiredMixin, ListView):
    """Класс представления для страницы со списком уроков"""
    template_name = 'lessons/lessons_list.html'
    context_object_name = 'lessons'
    paginate_by = 5

    def get_queryset(self):
        
        lessons = Lesson.objects.filter(pupil__owner=self.request.user).select_related('pupil', 'subject')

        pupil = self.request.GET.get('pupil', None)

        lesson_datetime = self.request.GET.get('lesson_datetime', None)

        subject = self.request.GET.get('subject', None)

        if pupil:
            lessons = lessons.filter(pupil__id=pupil)

        if lesson_datetime:
            # получаем объект datetime из запроса
            dt = timezone.datetime.strptime(lesson_datetime, '%Y-%m-%d %H:%M')
            # устанавливаем дате часовой пояс (иначе django ругается)
            dt = timezone.make_aware(dt, timezone.get_current_timezone())

            lessons = lessons.filter(lesson_datetime__date=dt.date(), lesson_datetime__time=dt.time())

        if subject:
            lessons = lessons.filter(subject__id=subject)

        return lessons
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # при создании формы передаём в неё пользователя
        context['form'] = LessonsFilterForm(data=self.request.GET, user=self.request.user) 
        context['title'] = 'L.A.S - Уроки'
        return context


class CreateLessonView(LoginRequiredMixin, CreateView):
    """Класс представления для страницы создания урока"""
    template_name = 'lessons/create_lesson.html'
    model = Lesson
    form_class = CreateLessonForm
    success_url = reverse_lazy('lessons:lessons_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'L.A.S - Создать урок'
        return context
    
    def get_form_kwargs(self):
        kwargs = super(CreateLessonView, self).get_form_kwargs()
        # при создании формы передаём в неё пользователя
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        return super().form_valid(form)


class UpdateLessonView(LoginRequiredMixin, UpdateView):
    """Класс представления для страницы обновления данных урока"""
    template_name = 'lessons/update_lesson.html'
    form_class = UpdateLessonForm
    model = Lesson
    context_object_name = 'lesson'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'L.A.S - Обновить данные урока'
        return context
    
    def get_form_kwargs(self):
        kwargs = super(UpdateLessonView, self).get_form_kwargs()
        # при создании формы передаём в неё пользователя
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        return super().form_valid(form)


class DeleteLessonView(LoginRequiredMixin, DeleteView):
    """Класс представления для удаления урока"""
    model = Lesson
    success_url = reverse_lazy('lessons:lessons_list')


class GetLessonDatetime(LoginRequiredMixin, View):
    """Класс представления для получения даты проведения урока"""
    def get_object(self, lesson_id, queryset=None):
        return Lesson.objects.get(id=lesson_id)
    
    def get(self, request, lesson_id):
        lesson = self.get_object(lesson_id)

        response_data = {'lesson_datetime': lesson.lesson_datetime}

        return JsonResponse(response_data)
