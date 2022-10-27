from rest_framework import serializers

from main.models import RolesTypeDictionary


class CodeRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolesTypeDictionary
        fields = ('code', 'name')
