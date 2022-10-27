"""
Здесь представлены базовые роли, которые необходимо создавать каждому пользователю
"""

MASTER_ROLE = {
    'name': 'Мастер',
    'description': 'Описание роли',
    'color': 'a531e7',
    'percentage': 100,
    'is_base': True,
    'type': 0,
    'project': None,
    'code': 1,
}

MENTOR_ROLE = {
    'name': 'Ментор',
    'description': 'Описание роли',
    'color': '97c4ed',
    'percentage': 100,
    'is_base': True,
    'type': 0,
    'project': None,
    'code': 2,
}

AUXILIARY_ROLE = {
    'name': 'Подсобный',
    'description': 'Описание роли',
    'color': 'ff9b39',
    'percentage': 80,
    'is_base': True,
    'type': 0,
    'project': None,
    'code': 3,
}

STUDENT_ROLE = {
    'name': 'Ученик',
    'description': 'Описание роли',
    'color': '14aaf6',
    'percentage': 60,
    'is_base': True,
    'type': 0,
    'project': None,
    'code': 4,
}

ACC_JOURNAL_ROLE = {
    'name': 'Журнал учета',
    'description': 'Описание роли',
    'color': '2a943a',
    'percentage': 3,
    'is_base': True,
    'type': 1,
    'project': None,
    'code': 5,
}

AMORTIZATION_INST_ROLE = {
    'name': 'Амортизация инструмента',
    'description': 'Описание роли',
    'color': 'eb96eb',
    'percentage': 10,
    'is_base': True,
    'type': 1,
    'project': None,
    'code': 6,
}

INTERN_ROLE = {
    'name': 'Испытательный срок',
    'description': 'Описание роли',
    'color': '838d0e',
    'amount': 0,
    'is_base': True,
    'type': 0,
    'project': None,
    'code': 7,
}

RESPONSIBLE_ROLE = {
    'name': 'Ответственный за размеры и качество',
    'description': 'Описание роли',
    'color': 'fccf04',
    'percentage': 10,
    'is_base': True,
    'type': 1,
    'project': None,
    'code': 8,
}
