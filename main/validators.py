import re


# Проверка на корректность названия задачи
def validate_name(name):
    if re.fullmatch('\s+', name) is None and name != '':
        return True
    return False
