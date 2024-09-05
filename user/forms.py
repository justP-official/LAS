from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm


class UserLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField()
    new_password1 = forms.CharField()
    new_password2 = forms.CharField()
    