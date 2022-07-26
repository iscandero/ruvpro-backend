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
        instance.save(update_field=['email', 'name', 'bio'])
        return instance
