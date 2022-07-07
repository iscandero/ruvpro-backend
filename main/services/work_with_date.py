from datetime import datetime


def convert_timestamp_to_date(timestamp):
    return datetime.fromtimestamp(timestamp).date()



