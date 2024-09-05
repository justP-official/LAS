from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from user.forms import UserLoginForm, UserPasswordChangeForm


class UserLogin(LoginView):
    """Класс представления для авторизации пользователя"""
    template_name = 'user/login.html'
    form_class = UserLoginForm
    extra_context = {'title': 'Easyhower - Войти',}


class UserProfile(LoginRequiredMixin, TemplateView):
    """Класс представления для отображения профиля пользователя"""
    template_name = 'user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserPasswordChangeForm(user=self.request.user)
        context['title'] = 'Easyhower - Профиль'
        return context
    

class UserPasswordChange(LoginRequiredMixin, PasswordChangeView):
    """Класс представления для смены пароля пользователя"""
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('user:profile')
    template_name = 'user/profile.html'