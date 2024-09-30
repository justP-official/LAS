from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.contrib import auth

class UserAppTestCase(TestCase):
    '''Набор тестов для приложения "user"'''

    def setUp(self) -> None:
        self.user_model = auth.get_user_model()
        self.user_data = {
            'username': 'test_user',
            'email': 'mail@gmail.com',
            'password': 'test_p@ssw0rd',
            'wrong_password': 'wrong_p@ssword',
            'new_password': 'n3w_p@ssword'
        }

        self.user = self.user_model.objects.create_user(
            username=self.user_data['username'], 
            email=self.user_data['email'],
            password=self.user_data['password']
        )

    def test_login(self):
        '''Тест страницы авторизации'''
        path = reverse('user:login')

        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['title'], 'L.A.S - Войти')
        self.assertTemplateUsed(response, 'user/login.html')

        response = self.client.post(path, data={
            'username': self.user_data['email'],
            'password': self.user_data['password']
            }
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_wrong_password(self):
        '''Тест авторизации с неправильным паролем'''
        path = reverse('user:login')
        response = self.client.post(path, data={
            'username': self.user_data['email'],
            'password': self.user_data['wrong_password']
            }
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response, 
            'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.'
        )
    
    def test_profile_page(self):
        '''Тест страницы профиля'''
        path = reverse('user:profile')

        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        self.client.force_login(self.user)

        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['title'], 'L.A.S - Профиль')
        self.assertTemplateUsed(response, 'user/profile.html')
        self.assertContains(response, f'Добро пожаловать, {self.user.email}')

    def test_password_change_form(self):
        '''Тест формы смены пароля'''
        self.client.force_login(self.user)

        password_change_path = reverse('user:password_change')

        response = self.client.post(password_change_path, data={
            'old_password': self.user_data['wrong_password'],
            'new_password1': self.user_data['new_password'],
            'new_password2': self.user_data['new_password'],
            }
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Ваш старый пароль введен неправильно. Пожалуйста, введите его снова.')

        response = self.client.post(password_change_path, data={
            'old_password': self.user_data['password'],
            'new_password1': self.user_data['wrong_password'],
            'new_password2': self.user_data['new_password'],
            }
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Введенные пароли не совпадают.')

        response = self.client.post(password_change_path, data={
            'old_password': self.user_data['password'],
            'new_password1': self.user_data['new_password'],
            'new_password2': self.user_data['new_password'],
            }
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
