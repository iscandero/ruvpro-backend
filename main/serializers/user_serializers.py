from rest_framework import serializers

from main.models import Role


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
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    bio = serializers.CharField(allow_null=True)
    email = serializers.EmailField()
    phone = serializers.CharField()
    authority = serializers.IntegerField()

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        instance.name = validated_data.get('bio', instance.bio)
        instance.save(update_fields=['email', 'name', 'bio'])
        return instance
