import re


def validate_name(name):
    if re.fullmatch('\s+', name) is None and name != '':
        return True
    return False


