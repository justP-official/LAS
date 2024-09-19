from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.template.loader import render_to_string
from django.contrib import auth

from user.forms import UserLoginForm


class MainAppTestCase(TestCase):
    """Набор тестов для приложения 'main'"""

    def test_index(self):
        """Тест страницы 'index'"""

        # переход на тестируемую страницу
        path = reverse('main:index')
        response = self.client.get(path)

        # проверка: код ответа должен быть == 200
        self.assertEqual(response.status_code, HTTPStatus.OK)

        # проверка: заголовок страницы
        self.assertEqual(response.context['title'], 'L.A.S - Главная')

        # проверка: шаблон страницы
        self.assertTemplateUsed(response, 'main/index.html')


    def test_form_render(self):
        """Тест отображения шаблонного тега формы"""

        # переход на тестируемую страницу
        path = reverse('main:index')
        response = self.client.get(path)

        # получение формы
        form = UserLoginForm()

        # рендер шаблонного тега формы
        form_html = render_to_string('main/templatetags_templates/form.html', context={'form': form})

        # проверка: присутствует ли форма на странице
        self.assertContains(response, form_html)

    def test_form_hidden(self):
        """Тест отсутствия формы при успешной авторизации"""

        # данные пользователя
        data = {
            'username': 'test_user',
            'password': 'test_p@ssw0rd',
            'email': 'mail@gmail.com'
        }

        # создание пользователя
        user_model = auth.get_user_model()
        user_model.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )

        # вход
        login_path = reverse('user:login')

        response = self.client.post(login_path, data={
            'username': data['email'],
            'password': data['password']
            }
        )

        # переход на тестируемую страницу
        index_path = reverse('main:index')
        response = self.client.get(index_path)

        # проверка: если фраза присутствует, то форма скрыта
        self.assertContains(response, 'Вы уже вошли')
