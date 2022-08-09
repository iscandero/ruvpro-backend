from main.models import CurrencyCourse
from datetime import date


def create_new_currency_pair_and_delete_old_pairs(pair: str, course: float):
    old_pairs = CurrencyCourse.objects.filter(pair=pair)
    if old_pairs:
        old_pairs.delete()
    CurrencyCourse.objects.create(pair=pair, price=course, date=date.today())
