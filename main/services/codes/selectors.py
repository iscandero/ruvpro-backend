from main.models import RolesTypeDictionary


def get_all_role_codes():
    return RolesTypeDictionary.objects.all()


def get_code_by_role_name(name: str) -> int:
    return RolesTypeDictionary.objects.filter(name=name).first().code
