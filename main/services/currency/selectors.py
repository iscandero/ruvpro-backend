from main.models import CurrencyCourse
from datetime import date


def get_currency_pair_today(pair: str):
    return CurrencyCourse.objects.filter(pair=pair, date=date.today()).first()


