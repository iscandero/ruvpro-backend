import datetime

from rest_framework import serializers

from main.services.work_with_date import convert_timestamp_to_date


class TimestampField(serializers.Field):
    def to_representation(self, value):
        value = datetime.datetime.combine(value, datetime.datetime.min.time())
        return value.timestamp()

    def to_internal_value(self, data):
        return convert_timestamp_to_date(float(data))