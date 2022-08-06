import requests


def get_convert_api_url(current_currency: str, need_currency: str):
    return f"https://currate.ru/api/?get=rates&pairs={current_currency + need_currency}&key=dfc54c39a00e467f6bdd9eb3e0c0de92"


def convert_currency(amount, current_currency: str, need_currency: str):
    response = requests.get(get_convert_api_url(current_currency=current_currency, need_currency=need_currency))
    json_resp = response.json()
    course = float(json_resp.get('data').get(f"{current_currency + need_currency}"))
    return amount * course


