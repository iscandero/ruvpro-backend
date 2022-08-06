from rest_framework import serializers
from main.services.statistic.use_cases import sum_queryset, avg_queryset, max_queryset, min_queryset


class WorkTimeSerializerForStatistics(serializers.Serializer):
    total = serializers.SerializerMethodField()
    min = serializers.SerializerMethodField()
    max = serializers.SerializerMethodField()
    average = serializers.SerializerMethodField()

    def get_total(self, user):
        times_queryset = self.context.get('times_queryset')
        return sum_queryset(queryset=times_queryset, field='work_time') * 3600

    def get_min(self, user):
        times_queryset = self.context.get('times_queryset')
        return min_queryset(queryset=times_queryset, field='work_time') * 3600

    def get_max(self, user):
        times_queryset = self.context.get('times_queryset')
        return max_queryset(queryset=times_queryset, field='work_time') * 3600

    def get_average(self, user):
        times_queryset = self.context.get('times_queryset')
        return avg_queryset(queryset=times_queryset, field='work_time') * 3600


class RateSerializerForStatistics(serializers.Serializer):
    min = serializers.SerializerMethodField()
    max = serializers.SerializerMethodField()
    average = serializers.SerializerMethodField()

    def get_min(self, user):
        rates_list = self.context.get('rates_list')
        return min(rates_list) if rates_list else 0

    def get_max(self, user):
        rates_list = self.context.get('rates_list')
        return max(rates_list) if rates_list else 0

    def get_average(self, user):
        rates_list = self.context.get('rates_list')
        len_rates = len(rates_list)
        return sum(rates_list) / len_rates if len_rates != 0 else 0


class SalarySerializerForStatistics(serializers.Serializer):
    total = serializers.SerializerMethodField()
    min = serializers.SerializerMethodField()
    max = serializers.SerializerMethodField()
    average = serializers.SerializerMethodField()

    def get_total(self, user):
        avg_rate = self.context.get('avg_rate')
        total_work_time = self.context.get('total_work_time') / 3600
        return total_work_time * avg_rate

    def get_min(self, user):
        avg_rate = self.context.get('avg_rate')
        min_work_time = self.context.get('min_work_time') / 3600
        return min_work_time * avg_rate

    def get_max(self, user):
        avg_rate = self.context.get('avg_rate')
        max_work_time = self.context.get('max_work_time') / 3600
        return max_work_time * avg_rate

    def get_average(self, user):
        avg_rate = self.context.get('avg_rate')
        avg_work_time = self.context.get('avg_work_time') / 3600
        return avg_work_time * avg_rate
