import os
import requests

from rest_framework.serializers import ValidationError
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('CONVERTER_API_KEY', None)

CURRENCIES = 'currencies'
RATES = 'latest'
SOURCE_URL = 'https://api.freecurrencyapi.com/v1/'


def _get_currencies_list():
    """
    Делает запрос к ресурсу для получения списка валют
    и возвращает словарь с информацией о валютах.
    """
    url = f'{SOURCE_URL}{CURRENCIES}?apikey={API_KEY}'
    currencies = requests.get(url).json()
    return currencies.get('data')


def get_currency_rate(from_currency: str, to_currency: str, value: int):
    """
    Делает запрос курса для валютной пары и возвращает
    итоговое значение после конвертации.
    """
    url = (
        f'{SOURCE_URL}{RATES}?apikey={API_KEY}'
        f'&currencies={to_currency}&base_currency={from_currency}'
    )
    rate_data = requests.get(url).json()
    rate = rate_data.get('data').get(to_currency)
    result = rate * value
    return round(result, 2)


def validate_query(from_currency, to_currency, value):
    """
    Валидирует запрос.
    Если какой-то параметр не заполнен, или число меньше или равно нулю,
    или запрошенной валюты нет в базе, выбрасывается исключение.
    """
    if not from_currency or not to_currency or (not value and value != 0):
        raise ValidationError(
            {'error':
             'Должны быть заполнены все параметры запроса.'})
    if value <= 0:
        raise ValidationError(
            {'error':
             f'Значение должно быть больше нуля: {value}'})
    currencies = [from_currency, to_currency]
    available_currencies = _get_currencies_list()
    for currency in currencies:
        if currency not in available_currencies:
            raise ValidationError(
                {'error': f'Такой валюты у нас нет: {currency}'})
