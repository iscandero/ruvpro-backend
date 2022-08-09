import requests

from main.services.currency.API.currency_converter_api import get_convert_api_url
from main.services.currency.interactors import create_new_currency_pair_and_delete_old_pairs
from main.services.currency.selectors import get_currency_pair_today


def convert_currency(amount, current_currency: str, need_currency: str):
    pair = current_currency + need_currency
    pair_from_db = get_currency_pair_today(pair=pair)
    if pair_from_db:
        course = pair_from_db.price
    else:
        response = requests.get(get_convert_api_url(current_currency=current_currency, need_currency=need_currency))
        json_resp = response.json()
        course = float(json_resp.get('data').get(f"{pair}"))
        create_new_currency_pair_and_delete_old_pairs(pair=pair, course=course)

    return amount * course
