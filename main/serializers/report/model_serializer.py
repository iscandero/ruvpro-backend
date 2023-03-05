from rest_framework import serializers

from main.models import Report


class ModelReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'