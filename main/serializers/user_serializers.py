from rest_framework import serializers

from main.models import Role


class RoleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(allow_null=True)
    color = serializers.CharField()
    percentage = serializers.FloatField(allow_null=True)
    amount = serializers.FloatField(allow_null=True)
    type = serializers.IntegerField()
    author_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        return Role.objects.create(**validated_data)
