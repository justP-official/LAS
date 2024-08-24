from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from user.forms import UserLoginForm, UserPasswordChangeForm

# Create your views here.
class UserLogin(LoginView):
    template_name = 'user/login.html'
    form_class = UserLoginForm
    extra_context = {'title': 'Easyhower - Войти',}


class UserProfile(LoginRequiredMixin, TemplateView):
    template_name = 'user/profile.html'
    extra_context = {'title': 'Easyhower - Профиль',}
    

class UserPasswordChange(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('user:profile')
    template_name = 'user/profile.html'