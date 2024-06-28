from django.test import TestCase
from rest_framework import status

from users.models import User


class UserTestCase(TestCase):

    def test_create_user_filling_required_field(self):
        """
        Тест проверяет на обязательное заполнение поля 'chat_id'.
        """
        data_user = {
            'email': 'test@test.com',
            'password': '12345',
        }
        response = self.client.post(
            '/users/create/',
            data=data_user
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            response.json(),
            {'chat_id': ['Обязательное поле.']}
        )

    def test_create_user(self):
        """
        Тест на создание нового пользователя.
        """
        data_user = {
            'email': 'test@test.com',
            'password': '12345',
            'chat_id': 1010101010,
        }
        response = self.client.post(
            '/users/create/',
            data=data_user
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.json().get('is_active') is not None and response.json().get('is_active'), True
        )

    def tearDown(self):
        """
        Очистка базы данных после выполнения каждого теста.
        """
        User.objects.all().delete()
