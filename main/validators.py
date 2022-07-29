import re


# Проверка на корректность названия задачи
from rest_framework import serializers

from main.const_data.currency_codes import currency_list


def validate_name(name):
    if re.fullmatch('\s+', name) is None and name != '':
        return True
    return False


def validate_currency(value):
    if (value, value) not in currency_list:
        raise serializers.ValidationError('Указана неверная валюта')
