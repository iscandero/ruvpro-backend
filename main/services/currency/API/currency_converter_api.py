def get_convert_api_url(current_currency: str, need_currency: str):
    return f"https://currate.ru/api/?get=rates&pairs={current_currency + need_currency}&key=19ef9838a245f3da8dd45abfb18f32d4"
