
from datetime import date
from decimal import Decimal

from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from reports.models import Report

from lessons.models import Lesson

from pupils.models import Pupil

from user.models import User

from subjects.models import Subjects


class ReportsAppTestCase(TestCase):
    '''Набор тестов для приложения "reports"'''

    fixtures = [
        'fixtures/user/users.json', 
        'fixtures/subjects/subjects.json', 
        'fixtures/pupils/pupils.json',
        'fixtures/lessons/lessons.json',
        'fixtures/reports/reports.json',
    ]

    def setUp(self) -> None:
        self.subjects = Subjects.objects.all()

        self.user_owner = User.objects.get(id=1)
        self.user_not_owner = User.objects.get(id=2)

        self.pupil = Pupil.objects.get(id=2)

        self.report_data = {
            'pupil': self.pupil.pk,
            'start_period': date(2024, 9, 1),
            'end_period': date(2024, 9, 30)
        }

        self.filters = {
            'pupil': self.pupil.pk,
            'start_period': date(2024, 9, 1).strftime('%Y-%m-%d'),
            'end_period': date(2024, 9, 11).strftime('%Y-%m-%d')
        }

    def test_redirect_reports_list(self):
        '''Тест перенаправления неавторизованного пользователя со страницы списка отчётов'''
        path = reverse('reports:reports_list')

        redirect_url = f"{reverse('user:login')}?next={path}"

        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_url)

    def test_reports_list(self):
        '''Тест страницы списка отчётов'''
        self.client.force_login(self.user_owner)

        path = reverse('reports:reports_list')

        paginate_by = 5

        reports = Report.objects.filter(pupil__owner=self.user_owner)
        
        response = self.client.get(path)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['title'], 'L.A.S - Отчёты')
        self.assertTemplateUsed(response, 'reports/reports_list.html')
        self.assertQuerySetEqual(response.context['reports'], reports[:paginate_by])

    def test_reports_list_paginate(self):
        '''Тест пагинации страницы списка отчётов'''
        self.client.force_login(self.user_owner)

        page = 2

        paginate_by = 5

        path = reverse('reports:reports_list')

        reports = Report.objects.filter(pupil__owner=self.user_owner)

        response = self.client.get(f'{path}?page={page}')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertQuerySetEqual(response.context['reports'], reports[(page - 1) * paginate_by : page * paginate_by])

    def test_reports_list_filters(self):
        '''Тест фильтрации страницы списка отчётов'''
        self.client.force_login(self.user_owner)

        path = reverse('reports:reports_list')

        paginate_by = 5

        query_params = '&'.join(f'{k}={v}' for k, v in self.filters.items())

        reports = Report.objects.filter(
            pupil__id=self.filters['pupil'],
            start_period__gte=self.filters['start_period'],
            end_period__lte=self.filters['end_period'],
        )

        response = self.client.get(f'{path}?{query_params}')

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertQuerySetEqual(response.context['reports'], reports[:paginate_by])

    def test_empty_reports_list(self):
        '''Тест страницы пустого списка отчётов'''
        self.client.force_login(self.user_not_owner)

        path = reverse('reports:reports_list')

        response = self.client.get(path)
        
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Ничего не найдено!')

    def test_create_report_page(self):
        '''Тест страницы добавления нового отчёта'''
        self.client.force_login(self.user_owner)

        path = reverse('reports:create_report')

        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['title'], 'L.A.S - Создать отчёт')
        self.assertTemplateUsed(response, 'reports/create_report.html')

    def test_redirect_create_report_page(self):
        '''Тест перенаправления неавторизованного пользователя со страницы добавления нового отчёта'''
        path = reverse('reports:create_report')

        response = self.client.get(path)

        redirect_url = f"{reverse('user:login')}?next={path}"

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_url)

    def test_create_report(self):
        '''Тест добавления нового отчёта'''
        self.client.force_login(self.user_owner)

        path = reverse('reports:create_report')

        response = self.client.post(path, data=self.report_data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('reports:read_report', kwargs={'report_id': Report.objects.first().pk}))
        self.assertTrue(Report.objects.filter(
            pupil__id=self.report_data['pupil'],
            start_period=self.report_data['start_period'],
            end_period=self.report_data['end_period'],
            ).exists()
        )

    def test_create_report_wrong_data(self):
        '''Тест добавления нового отчёта с неверными данными'''
        self.report_data['pupil'] = -1

        self.client.force_login(self.user_owner)

        path = reverse('reports:create_report')

        response = self.client.post(path, data=self.report_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Выберите корректный вариант. Вашего варианта нет среди допустимых значений')

    def test_read_report(self):
        '''Тест страницы просмотра отчёта'''
        self.client.force_login(self.user_owner)

        path = reverse('reports:read_report', kwargs={'report_id': 1})

        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['title'], 'L.A.S - Просмотр отчёта')
        self.assertTemplateUsed(response, 'reports/read_report.html')
    
    def test_redirect_read_report_page(self):
        '''Тест перенаправления неавторизованного пользователя со страницы просмотра отчёта'''
        path = reverse('reports:read_report', kwargs={'report_id': 1})

        response = self.client.get(path)

        redirect_url = f"{reverse('user:login')}?next={path}"

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_url)

    def test_read_report_forbidden(self):
        '''Тест запрета просмотра чужого отчёта'''
        self.client.force_login(self.user_not_owner)

        path = reverse('reports:read_report', kwargs={'report_id': 1})

        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, '403')


    def test_update_report_page(self):
        '''Тест страницы обновления данных отчёта'''
        self.client.force_login(self.user_owner)

        path = reverse('reports:update_report', kwargs={'report_id': 1})

        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context['title'], 'L.A.S - Обновить данные отчёта')
        self.assertTemplateUsed(response, 'reports/update_report.html')

    def test_redirect_update_report_page(self):
        '''Тест перенаправления неавторизованного пользователя со страницы обновления данных отчёта'''
        path = reverse('reports:update_report', kwargs={'report_id': 1})

        response = self.client.get(path)

        redirect_url = f"{reverse('user:login')}?next={path}"

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, redirect_url)

    def test_update_report(self):
        '''Тест обновления данных отчёта'''
        self.client.force_login(self.user_owner)

        path = reverse('reports:update_report', kwargs={'report_id': 1})

        response = self.client.post(path, data=self.report_data)

        report = Report.objects.get(pk=1)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('reports:read_report', kwargs={'report_id': 1}))

        for key, value in self.report_data.items():
            if key == 'pupil':
                self.assertEqual(getattr(report, key).pk, value)
            else:
                self.assertEqual(getattr(report, key), value)

    def test_update_report_wrong_data(self):
        '''Тест страницы обновления данных отчёта с неверными данными'''
        self.report_data['pupil'] = -1

        self.client.force_login(self.user_owner)

        path = reverse('reports:update_report', kwargs={'report_id': 1})

        response = self.client.post(path, data=self.report_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Выберите корректный вариант. Вашего варианта нет среди допустимых значений')

    def test_update_report_forbidden(self):
        '''Тест запрета обновления чужого отчёта'''
        self.client.force_login(self.user_not_owner)

        path = reverse('reports:update_report', kwargs={'report_id': 1})

        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, '403')

        response = self.client.post(path, data=self.report_data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, '403')

    def test_delete_report(self):
        '''Тест удаления отчёта'''
        self.client.force_login(self.user_owner)

        path = reverse('reports:delete_report', kwargs={'report_id': 1})

        response = self.client.post(path)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('reports:reports_list'))

        path = reverse('reports:update_report', kwargs={'report_id': 1})

        response = self.client.get(path)

        self.assertContains(response, 404)

        report = Report.objects.filter(id=1).first()

        self.assertFalse(report)

    def test_update_report_forbidden(self):
        '''Тест запрета удаления чужого отчёта'''
        self.client.force_login(self.user_not_owner)

        path = reverse('reports:delete_report', kwargs={'report_id': 1})

        response = self.client.post(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, '403')
