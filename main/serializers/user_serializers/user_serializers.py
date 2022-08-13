from rest_framework import serializers
from main.models import Role, SocialNetworks, AppUser


class RoleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=False)
    description = serializers.CharField(allow_null=True, required=False)
    color = serializers.CharField(required=False)
    percentage = serializers.FloatField(allow_null=True, required=False)
    amount = serializers.FloatField(allow_null=True, required=False)
    type = serializers.IntegerField(required=False)

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
            instance.amount = validated_data.get('amount', instance.amount)
            instance.save(update_fields=['amount'])
        return instance


class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialNetworks
        fields = ('name', 'url')


class CurrencyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ('currency',)


class UserSerializerForOutput(serializers.ModelSerializer):
    social = SocialSerializer(many=True, source='socials')

    class Meta:
        model = AppUser
        fields = ('id', 'name', 'bio', 'email', 'phone', 'authority', 'avatar', 'social')


class UserSerializerForUpdate(serializers.Serializer):
    id = serializers.IntegerField(read_only=True, required=False)
    name = serializers.CharField(required=False)
    bio = serializers.CharField(allow_null=True, allow_blank=True, required=False)
    email = serializers.EmailField(required=False)
    phone = serializers.CharField(required=False)
    authority = serializers.IntegerField(required=False)
    currency = serializers.CharField(required=False)
    avatar = serializers.URLField(allow_null=True, allow_blank=True, required=False)
    social = SocialSerializer(many=True, required=False, source='socials')

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
        if validated_data.get('authority') is not None:
            instance.authority = validated_data.get('authority', instance.authority)
            update_fields.append('authority')
        if validated_data.get('avatar') is not None:
            instance.avatar = validated_data.get('avatar', instance.avatar)
            update_fields.append('avatar')

        socials = validated_data.get('socials')
        if socials is not None:
            for social in socials:
                social_name = social['name']
                social_url = social['url']
                if social_name in instance.socials.values_list('name', flat=True):
                    need_social = instance.socials.get(name=social_name)
                    need_social.url = social_url
                    need_social.save()
                else:
                    new_social = SocialNetworks.objects.create(name=social_name, url=social_url)
                    instance.socials.add(new_social)

        instance.save(update_fields=update_fields)
        return instance
