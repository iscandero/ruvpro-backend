from main.models import CurrencyCourse
from datetime import date


def create_new_currency_pair_and_delete_old_pairs(pair: str, course: float):
    CurrencyCourse.objects.filter(pair=pair).delete()
    CurrencyCourse.objects.create(pair=pair, price=course, date=date.today())
