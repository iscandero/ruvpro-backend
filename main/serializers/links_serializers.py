from rest_framework import serializers

from main.models import Link


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ('name', 'url')
