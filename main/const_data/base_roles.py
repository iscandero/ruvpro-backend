"""
Здесь представлены базовые роли, которые необходимо создавать каждому платному пользователю
"""

MASTER_ROLE = {
    'name': 'Мастер',
    'description': 'Описание роли',
    'color': 'a531e7',
    'percentage': 100,
    'is_base': True,
    'type': 0,
    'project': None,
}

MENTOR_ROLE = {
    'name': 'Ментор',
    'description': 'Описание роли',
    'color': '97c4ed',
    'percentage': 100,
    'is_base': True,
    'type': 0,
    'project': None,
}

AUXILIARY_ROLE = {
    'name': 'Подсобный',
    'description': 'Описание роли',
    'color': 'ff9b39',
    'percentage': 80,
    'is_base': True,
    'type': 0,
    'project': None,
}

STUDENT_ROLE = {
    'name': 'Ученик',
    'description': 'Описание роли',
    'color': '14aaf6',
    'percentage': 60,
    'is_base': True,
    'type': 0,
    'project': None,
}

ACC_JOURNAL_ROLE = {
    'name': 'Журнал учета',
    'description': 'Описание роли',
    'color': '2a943a',
    'percentage': 3,
    'is_base': True,
    'type': 1,
    'project': None,
}

AMORTIZATION_INST_ROLE = {
    'name': 'Аммортизация инструмента',
    'description': 'Описание роли',
    'color': 'eb96eb',
    'percentage': 10,
    'is_base': True,
    'type': 1,
    'project': None,
}

INTERN_ROLE = {
    'name': 'Испытательный срок',
    'description': 'Описание роли',
    'color': '838d0e',
    'amount': 0,
    'is_base': True,
    'type': 0,
    'project': None,
}

RESPONSIBLE_ROLE = {
    'name': 'Ответственный за размеры и качество',
    'description': 'Описание роли',
    'color': 'fccf04',
    'percentage': 10,
    'is_base': True,
    'type': 1,
    'project': None,
}