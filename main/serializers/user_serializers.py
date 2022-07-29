from rest_framework import serializers

from main.models import Role
from main.validators import validate_currency


class RoleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False)
    description = serializers.CharField(allow_null=True, required=False)
    color = serializers.CharField(required=False)
    percentage = serializers.FloatField(allow_null=True, required=False)
    amount = serializers.FloatField(allow_null=True, required=False)
    type = serializers.IntegerField(required=False)
    author_id = serializers.IntegerField(write_only=True, required=False)

    def create(self, validated_data):
        return Role.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.color = validated_data.get('color', instance.color)
        instance.save(update_fields=['name', 'description', 'color'])

        if validated_data.get('percentage') is not None:
            instance.percentage = validated_data.get('percentage', instance.percentage)
            instance.save(update_fields=['percentage'])

        if validated_data.get('amount') is not None:
            instance.percentage = validated_data.get('amount', instance.amount)
            instance.save(update_fields=['amount'])
        return instance


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, required=False)
    name = serializers.CharField(required=False)
    bio = serializers.CharField(allow_null=True, required=False)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)
    authority = serializers.IntegerField(required=False)
    currency = serializers.CharField(required=False, validators=[validate_currency])

    def update(self, instance, validated_data):
        update_fields = []
        if validated_data.get('email') is not None:
            instance.email = validated_data.get('email', instance.email)
            update_fields.append('email')
        if validated_data.get('name') is not None:
            instance.name = validated_data.get('name', instance.name)
            update_fields.append('name')
        if validated_data.get('bio') is not None:
            instance.bio = validated_data.get('bio', instance.bio)
            update_fields.append('bio')
        if validated_data.get('currency') is not None:
            instance.currency = validated_data.get('currency', instance.currency)
            update_fields.append('currency')
        instance.save(update_fields=update_fields)
        return instance
