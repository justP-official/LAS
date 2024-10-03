
from datetime import date
from decimal import Decimal

from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from lessons.models import Lesson

from pupils.models import Pupil

from user.models import User

from subjects.models import Subjects


class LessonsAppTestCase(TestCase):
    '''Набор тестов для приложения "lessons"'''

    fixtures = [
        'fixtures/user/users.json', 
        'fixtures/subjects/subjects.json', 
        'fixtures/pupils/pupils.json',
        'fixtures/lessons/lessons.json'
    ]

    def setUp(self) -> None:
        self.subjects = Subjects.objects.all()

        self.user_owner = User.objects.get(id=1)
        self.user_not_owner = User.objects.get(id=2)

        self.pupil = Pupil.objects.get(id=2)

        self.lesson_data = {
            'pupil': self.pupil.pk,
            'subject': self.subjects[0].pk,
            'lesson_datetime': timezone.datetime(2024, 10, 2, 18, 00, 00, tzinfo=timezone.get_current_timezone()),
            'lesson_duration': Decimal('1.5'),
            'money_recived': Decimal('1050')
        }

        self.filters = {
            'pupil': self.pupil.pk,
            'subject': self.subjects[1].pk,
            'lesson_date': date(2024, 9, 8).strftime('%Y-%m-%d')
        }

    def test_redirect_lessons_list(self):
        '''Тест перенаправления неавторизованного пользователя со страницы списка уроков'''
        path = reverse('lessons:lessons_list')

        redirect_url = f"{reverse('user:login')}?next={path}"

        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_url)

    def test_lessons_list(self):
        '''Тест страницы списка уроков'''
        self.client.force_login(self.user_owner)

        path = reverse('lessons:lessons_list')

        paginate_by = 5

        lessons = Lesson.objects.filter(pupil__owner=self.user_owner)
        
        response = self.client.get(path)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['title'], 'L.A.S - Уроки')
        self.assertTemplateUsed(response, 'lessons/lessons_list.html')
        self.assertQuerySetEqual(response.context['lessons'], lessons[:paginate_by])

    def test_lessons_list_paginate(self):
        '''Тест пагинации страницы списка уроков'''
        self.client.force_login(self.user_owner)

        page = 2

        paginate_by = 5

        path = reverse('lessons:lessons_list')

        lessons = Lesson.objects.filter(pupil__owner=self.user_owner)

        response = self.client.get(f'{path}?page={page}')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertQuerySetEqual(response.context['lessons'], lessons[(page - 1) * paginate_by : page * paginate_by])

    def test_lessons_list_filters(self):
        '''Тест фильтрации страницы списка уроков'''
        self.client.force_login(self.user_owner)

        path = reverse('lessons:lessons_list')

        paginate_by = 5

        query_params = '&'.join(f'{k}={v}' for k, v in self.filters.items())

        lessons = Lesson.objects.filter(
            pupil__id=self.filters['pupil'],
            lesson_datetime__date=self.filters['lesson_date'],
            subject__id=self.filters['subject']
        )

        response = self.client.get(f'{path}?{query_params}')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertQuerySetEqual(response.context['lessons'], lessons[:paginate_by])

    def test_empty_lessons_list(self):
        '''Тест страницы пустого списка уроков'''
        self.client.force_login(self.user_not_owner)

        path = reverse('lessons:lessons_list')

        response = self.client.get(path)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Ничего не найдено!')

    def test_create_lesson_page(self):
        '''Тест страницы добавления нового урока'''
        self.client.force_login(self.user_owner)

        path = reverse('lessons:create_lesson')

        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['title'], 'L.A.S - Создать урок')
        self.assertTemplateUsed(response, 'lessons/create_lesson.html')

    def test_redirect_create_lesson_page(self):
        '''Тест перенаправления неавторизованного пользователя со страницы добавления нового урока'''
        path = reverse('lessons:create_lesson')

        response = self.client.get(path)

        redirect_url = f"{reverse('user:login')}?next={path}"

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_url)

    def test_create_lesson(self):
        '''Тест добавления нового урока'''
        self.client.force_login(self.user_owner)

        path = reverse('lessons:create_lesson')

        response = self.client.post(path, data=self.lesson_data)

        print(response.content.decode())

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('lessons:lessons_list'))
        self.assertTrue(Lesson.objects.filter(lesson_datetime=self.lesson_data['lesson_datetime']).exists())


    def test_create_lesson_wrong_data(self):
        '''Тест добавления нового урока с неверными данными'''
        self.lesson_data['lesson_duration'] = Decimal('0.15')

        self.client.force_login(self.user_owner)

        path = reverse('lessons:create_lesson')

        response = self.client.post(path, data=self.lesson_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Слишком короткий урок')

    def test_update_lesson_page(self):
        '''Тест страницы обновления данных урока'''
        self.client.force_login(self.user_owner)

        path = reverse('lessons:update_lesson', kwargs={'pk': 1})

        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['title'], 'L.A.S - Обновить данные урока')
        self.assertTemplateUsed(response, 'lessons/update_lesson.html')

    def test_redirect_update_lesson_page(self):
        '''Тест перенаправления неавторизованного пользователя со страницы обновления данных урока'''
        path = reverse('lessons:update_lesson', kwargs={'pk': 1})

        response = self.client.get(path)

        redirect_url = f"{reverse('user:login')}?next={path}"

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_url)

    def test_update_lesson(self):
        '''Тест обновления данных урока'''
        self.client.force_login(self.user_owner)

        path = reverse('lessons:update_lesson', kwargs={'pk': 1})

        response = self.client.post(path, data=self.lesson_data)

        lesson = Lesson.objects.get(pk=1)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, path)

        for key, value in self.lesson_data.items():
            if key in ('pupil', 'subject'):
                self.assertEqual(getattr(lesson, key).pk, value)
            else:
                self.assertEqual(getattr(lesson, key), value)

    def test_update_lesson_wrong_data(self):
        '''Тест страницы обновления данных урока с неверными данными'''
        self.lesson_data['lesson_duration'] = Decimal('0.15')

        self.client.force_login(self.user_owner)

        path = reverse('lessons:update_lesson', kwargs={'pk': 1})

        response = self.client.post(path, data=self.lesson_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Слишком короткий урок')

    def test_delete_lesson(self):
        '''Тест удаления урока'''
        self.client.force_login(self.user_owner)

        path = reverse('lessons:delete_lesson', kwargs={'pk': 1})

        response = self.client.post(path)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('lessons:lessons_list'))

        path = reverse('lessons:update_lesson', kwargs={'pk': 1})

        response = self.client.get(path)

        self.assertContains(response, 404)

        lesson = Lesson.objects.filter(id=1).first()

        self.assertFalse(lesson)
