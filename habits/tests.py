from datetime import timedelta, time

from django_celery_beat.models import PeriodicTask
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='tetst@test.com', password='test', chat_id='0101010101')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        self.habit = Habit.objects.create(
            owner=self.user,
            place='Спальная комната',
            time=time(7, 00),
            action='Сделать зарядку',
            nice_habit=True,
            period=1,
            time_execution=timedelta(minutes=2),
            is_public=True
        )

    def test_create_habit(self):
        """
        Тест на создание привычки.
        """
        data_habit = {
            'place': 'Любое',
            'time': '09:00:00',
            'action': 'Планирование задач',
            'nice_habit': True,
            'period': 1,
            'time_execution': '00:02:00',
            'is_public': True
        }
        response = self.client.post(
            '/habits/create/',
            data=data_habit
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json(),
            {
                'id': self.habit.id + 1,
                'place': 'Спальная комната',
                'time': '07:00:00',
                'action': 'Сделать зарядку',
                'nice_habit': True,
                'related_habit': None,
                'period': 1,
                'reward': None,
                'time_execution': '00:02:00',
                'is_public': True
            }
        )

    def test_create_habit_filling_required_field(self):
        """
        Тест проверяет на обязательное заполнение поля 'action'.
        """
        data_habit = {
            'place': 'Любое',
            'time': '09:00:00',
            'action': 'Планирование задач',
            'nice_habit': True,
            'period': 1,
            'time_execution': '00:02:00',
            'is_public': True
        }
        response = self.client.post(
            '/habits/create/',
            data=data_habit
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'action': ['Обязательное поле']},
        )

    def test_create_habit_select_related_habit_or_reward(self):
        """
        Тест проверяет на одновременное использование связанной привычки и вознаграждения.
        """
        data_habit = {
            'place': 'Любое',
            'time': '09:00:00',
            'action': 'Планирование задач',
            'nice_habit': True,
            'period': 1,
            'time_execution': '00:02:00',
            'is_public': True
        }
        response = self.client.post(
            '/habits/create/',
            data=data_habit
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Нельзя одновременно указывать связанную привычку и вознаграждение.']}
        )

    def test_create_habit_execution_time_no_more_120_seconds(self):
        """
        Тест проверяет на использование времени для выполнения привычки более 120 секунд.
        """
        data_habit = {
            'place': 'Любое',
            'time': '09:00:00',
            'action': 'Планирование задач',
            'nice_habit': True,
            'period': 1,
            'time_execution': '00:02:00',
            'is_public': True
        }
        response = self.client.post(
            '/habits/create/',
            data=data_habit
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['Время на выполнение не должно превышать 120 секунд.']}
        )

    def test_create_habit_only_nice_habit_into_related_habit(self):
        """
        Тест проверяет на использование в связанных привычках только приятные привычки.
        """
        data_habit = {
            'place': 'Любое',
            'time': '09:00:00',
            'action': 'Планирование задач',
            'nice_habit': True,
            'period': 1,
            'time_execution': '00:02:00',
            'is_public': True
        }
        response = self.client.post(
            '/habits/create/',
            data=data_habit
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['В связанные привычки могут попадать только привычки с признаком приятной привычки.']}
        )

    def test_create_nice_habit_cannot_have_reward_or_related_habit(self):
        """
        Тест проверяет на использование у приятной привычки вознаграждения или связанной привычки.
        """
        data_habit = {
            'place': 'Любое',
            'time': '09:00:00',
            'action': 'Планирование задач',
            'nice_habit': True,
            'period': 1,
            'time_execution': '00:02:00',
            'is_public': True
        }
        response = self.client.post(
            '/habits/create/',
            data=data_habit
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'non_field_errors': ['У приятной привычки не может быть вознаграждения или связанной привычки.']}
        )

    def test_create_habit_periodic_task(self):
        """
        Тест проверяет корректность создания периодической задачи привычки.
        """
        data_habit = {
            'place': 'Любое',
            'time': '09:00:00',
            'action': 'Планирование задач',
            'nice_habit': True,
            'period': 1,
            'time_execution': '00:02:00',
            'is_public': True
        }
        response = self.client.post(
            '/habits/create/',
            data=data_habit
        )
        self.assertEqual(
            PeriodicTask.objects.filter(name=f'HabitTask{self.habit.id + 1}').exists(), True
        )

    def test_list_habit(self):
        """
        Тест проверяет, что список привычек успешно загружается и содержит 4 привычки.
        """
        response = self.client.get(
            '/habits/list/',
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json().get('count') is not None and response.json().get('count') == 4, True
        )

    def test_view_habit(self):
        """
        Тест на корректное возвращение данных о привычке по ее id и что данные соответствуют ожидаемым.
        """
        response = self.client.get(
            f'/habits/view/{self.habit.id}/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                'id': self.habit.id,
                'place': self.habit.place,
                'time': self.habit.time,
                'action': self.habit.action,
                'nice_habit': True,
                'related_habit': None,
                'period': self.habit.period,
                'reward': None,
                'time_execution': self.habit.time_execution,
                'is_public': True,
                'owner': self.habit.owner,
            }
        )

    def test_update_habit(self):
        """
        Тест помогает убедиться, что функция обновления привычки возвращает
        корректный ответ и обновляет данные в соответствии с ожидаемыми значениями.
        """
        data_habit = {
            'id': self.habit.id,
            'place': self.habit.place,
            'time': self.habit.time,
            'action': 'Test',
            'nice_habit': True,
            'period': self.habit.period,
            'time_execution': self.habit.time_execution,
            'is_public': True,
            'owner': self.habit.owner,
        }
        response = self.client.patch(
            f'/habits/update/{self.habit.id}/',
            data=data_habit
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json(),
            {
                'id': self.habit.id,
                'place': self.habit.place,
                'time': self.habit.time,
                'action': 'Test',
                'nice_habit': True,
                'period': self.habit.period,
                'time_execution': self.habit.time_execution,
                'is_public': True,
                'owner': self.habit.owner,
            }
        )

    def test_delete_habit(self):
        """
        Тест для проверки корректности работы функционала удаления и
        защиты от случайного или нежелательного удаления данных.
        """
        response = self.client.delete(
            f'/habits/delete/{self.habit.id}/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_list_habit_public(self):
        """
        Тест проверяет, что метод возвращает публичные привычки и что возвращается ожидаемая информация.
        """
        response = self.client.get(
            '/habits/list_public/'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.json()[0].get('id') is not None and response.json()[0].get('id') == self.habit.id, True,
        )

    def tearDown(self):
        """
        Очистка базы данных после выполнения каждого теста.
        """
        Habit.objects.all().delete()
