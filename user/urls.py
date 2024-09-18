from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView

from user import views

app_name = 'user'

urlpatterns = [
    path('', views.UserProfile.as_view(), name='profile'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('password-change/', views.UserPasswordChange.as_view(), name='password_change'),
    path('password-reset/', PasswordResetView.as_view(
        template_name='user/password_reset_form.html', 
        email_template_name='user/password_reset_email.html',
        success_url=reverse_lazy('user:password_reset_done')
        ), 
        name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='user/password_reset_confirm.html',
        success_url=reverse_lazy('user:password_reset_complete')
        ), 
        name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'), name='password_reset_complete'),
    path('logout/', LogoutView.as_view(), name='logout'),
]