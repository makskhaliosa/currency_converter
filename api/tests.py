from django.test import TestCase, Client
from rest_framework import status

from .core.utils import get_currency_rate


class RatesTest(TestCase):
    """Тесты для Rate."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        # параметры запросов
        cls.usd = 'USD'
        cls.rub = 'RUB'
        cls.nonexisting = 'NONEXISTING'
        cls.eur = 'EUR'
        cls.yena = 'JPY'
        cls.positive = 1000
        cls.negative = -1
        cls.zero = 0
        # url для запросов
        cls.query_url = 'http://127.0.0.1:8000/api/rates?'
        cls.from_cur = 'from='
        cls.to_cur = '&to='
        cls.value = '&value='
        cls.success_url = (
            f'{cls.query_url}{cls.from_cur}{cls.usd}'
            f'{cls.to_cur}{cls.eur}{cls.value}{cls.positive}')
        cls.error_negative = (
            f'{cls.query_url}{cls.from_cur}{cls.rub}'
            f'{cls.to_cur}{cls.yena}{cls.value}{cls.negative}')
        cls.error_zero = (
            f'{cls.query_url}{cls.from_cur}{cls.rub}'
            f'{cls.to_cur}{cls.yena}{cls.value}{cls.zero}')
        cls.error_nonexisting = (
            f'{cls.query_url}{cls.from_cur}{cls.nonexisting}'
            f'{cls.to_cur}{cls.yena}{cls.value}{cls.positive}')
        cls.error_param_missing = (
            f'{cls.query_url}{cls.from_cur}{cls.rub}'
            f'{cls.to_cur}{cls.yena}')

    def test_success_query(self):
        """Проверяет, что все работает при корректном запросе."""
        response = self.client.get(self.success_url)
        rate = get_currency_rate(self.usd, self.eur, self.positive)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('result'), rate)

    def test_error_negative(self):
        """
        Проверяет, что выбрасывается верное исключение
        при отрицательном числе.
        """
        response = self.client.get(self.error_negative)
        data = f'Значение должно быть больше нуля: {self.negative}'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('error'), data)

    def test_error_zero(self):
        """
        Проверяет, что выбрасывается верное исключение при нуле.
        """
        response = self.client.get(self.error_zero)
        data = f'Значение должно быть больше нуля: {self.zero}'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('error'), data)

    def test_error_nonexisting(self):
        """
        Проверяет, что выбрасывается верное исключение
        при запросе несуществующей или недоступной валюты.
        """
        response = self.client.get(self.error_nonexisting)
        data = f'Такой валюты у нас нет: {self.nonexisting}'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('error'), data)

    def test_error_param_missing(self):
        """
        Проверяет, что выбрасывается верное исключение
        при отсутствии одного из параметров.
        """
        response = self.client.get(self.error_param_missing)
        data = 'Должны быть заполнены все параметры запроса.'
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get('error'), data)
