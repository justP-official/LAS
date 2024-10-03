from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from pupils.models import Pupil

from user.models import User

from subjects.models import Subjects


class PupilsAppTestCase(TestCase):
    '''Набор тестов для приложения "pupils"'''

    fixtures = ['fixtures/user/users.json', 'fixtures/subjects/subjects.json', 'fixtures/pupils/pupils.json']

    def setUp(self) -> None:
        self.subjects = Subjects.objects.all()

        self.user_owner = User.objects.get(id=1)
        self.user_not_owner = User.objects.get(id=2)

        self.pupil_data = {
            'name': 'Test name',
            'description': 'Test description',
            'price_per_hour': 700,
            'class_counter': 9,
            'is_active': True,
            'skype_only': True,
            'subjects': [subject.pk for subject in self.subjects],
            'owner': self.user_owner
        }

        self.filters = {
            'class_counter': 9,
            'skype_only': True,
            'subjects': 1
        }

    def test_redirect_pupils_list(self):
        '''Тест перенаправления неавторизованного пользователя со страницы списка учеников'''
        path = reverse('pupils:pupils_list')

        redirect_url = f"{reverse('user:login')}?next={path}"

        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_url)

    def test_pupils_list(self):
        '''Тест страницы списка учеников'''
        self.client.force_login(self.user_owner)

        path = reverse('pupils:pupils_list')

        paginate_by = 5

        pupils = Pupil.objects.filter(owner=self.user_owner).exclude(is_active=False)
        
        response = self.client.get(path)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['title'], 'L.A.S - Ученики')
        self.assertTemplateUsed(response, 'pupils/pupils_list.html')
        self.assertQuerySetEqual(response.context['pupils'], pupils[:paginate_by])

    def test_pupils_list_paginate(self):
        '''Тест пагинации страницы списка учеников'''
        self.client.force_login(self.user_owner)

        page = 2

        paginate_by = 5

        path = reverse('pupils:pupils_list')

        pupils = Pupil.objects.filter(owner=self.user_owner).exclude(is_active=False)

        response = self.client.get(f'{path}?page={page}')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertQuerySetEqual(response.context['pupils'], pupils[(page - 1) * paginate_by : page * paginate_by])

    def test_pupils_list_filters(self):
        '''Тест фильтрации страницы списка учеников'''
        self.client.force_login(self.user_owner)

        path = reverse('pupils:pupils_list')

        paginate_by = 5

        query_params = '&'.join(f'{k}={v}' for k, v in self.filters.items())

        pupils = Pupil.objects.filter(
            owner=self.user_owner,
            class_counter=self.pupil_data['class_counter'],
            is_active=self.pupil_data['is_active'],
            skype_only=self.pupil_data['skype_only']
        )

        response = self.client.get(f'{path}?{query_params}')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertQuerySetEqual(response.context['pupils'], pupils[:paginate_by])

    def test_empty_pupils_list(self):
        '''Тест страницы пустого списка учеников'''
        self.client.force_login(self.user_not_owner)

        path = reverse('pupils:pupils_list')

        response = self.client.get(path)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Ничего не найдено!')

    def test_create_pupil_page(self):
        '''Тест страницы добавления нового ученика'''
        self.client.force_login(self.user_owner)

        path = reverse('pupils:create_pupil')

        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['title'], 'L.A.S - Добавить ученика')
        self.assertTemplateUsed(response, 'pupils/create_pupil.html')

    def test_redirect_create_pupil_page(self):
        '''Тест перенаправления неавторизованного пользователя со страницы добавления нового ученика'''
        path = reverse('pupils:create_pupil')

        response = self.client.get(path)

        redirect_url = f"{reverse('user:login')}?next={path}"

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_url)

    def test_create_pupil(self):
        '''Тест добавления нового ученика'''
        self.client.force_login(self.user_owner)

        path = reverse('pupils:create_pupil')

        response = self.client.post(path, data=self.pupil_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('pupils:pupils_list'))
        self.assertTrue(Pupil.objects.filter(name=self.pupil_data['name']).exists())

        self.assertTrue(Pupil.objects.filter(name=self.pupil_data['name'])[0].owner == self.user_owner)

    def test_create_pupil_wrong_data(self):
        '''Тест добавления нового ученика с неверными данными'''
        self.pupil_data['class_counter'] = 4

        self.client.force_login(self.user_owner)

        path = reverse('pupils:create_pupil')

        response = self.client.post(path, data=self.pupil_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Убедитесь, что это значение больше либо равно 5')

    def test_create_pupil_exists_error(self):
        '''Тест невозможности добавления учеников с одинаковым именем'''
        Pupil.objects.create(
            name=self.pupil_data['name'], 
            class_counter=self.pupil_data['class_counter'], 
            owner=self.user_owner
        )

        self.client.force_login(self.user_owner)

        path = reverse('pupils:create_pupil')

        response = self.client.post(path, data=self.pupil_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Ученик с таким Имя уже существует')

    def test_update_pupil_page(self):
        '''Тест страницы обновления данных ученика'''
        self.client.force_login(self.user_owner)

        path = reverse('pupils:update_pupil', kwargs={'pk': 1})

        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['title'], 'L.A.S - Обновить данные ученика')
        self.assertTemplateUsed(response, 'pupils/update_pupil.html')

    def test_redirect_update_pupil_page(self):
        '''Тест перенаправления неавторизованного пользователя со страницы обновления данных ученика'''
        path = reverse('pupils:update_pupil', kwargs={'pk': 1})

        response = self.client.get(path)

        redirect_url = f"{reverse('user:login')}?next={path}"

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_url)

    def test_update_pupil(self):
        '''Тест обновления данных ученика'''
        self.client.force_login(self.user_owner)

        path = reverse('pupils:update_pupil', kwargs={'pk': 1})

        response = self.client.post(path, data=self.pupil_data)

        pupil = Pupil.objects.get(id=1)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, path)
        self.assertEqual(pupil.name, self.pupil_data['name'])

    def test_update_pupil_wrong_data(self):
        '''Тест страницы обновления данных ученика с неверными данными'''
        self.pupil_data['class_counter'] = 4

        self.client.force_login(self.user_owner)

        path = reverse('pupils:update_pupil', kwargs={'pk': 1})

        response = self.client.post(path, data=self.pupil_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Убедитесь, что это значение больше либо равно 5')

    def test_update_pupil_exists_error(self):
        '''Тест невозможности обновления одинаковым именем'''
        Pupil.objects.create(
            name=self.pupil_data['name'], 
            class_counter=self.pupil_data['class_counter'], 
            owner=self.user_owner
        )

        self.client.force_login(self.user_owner)

        path = reverse('pupils:update_pupil', kwargs={'pk': 1})

        response = self.client.post(path, data=self.pupil_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Ученик с таким Имя уже существует')
