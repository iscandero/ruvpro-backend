from rest_framework import serializers

from main.models import ProjectEmployee, AppUser, Team
from main.serializers.user_serializers.user_serializers import UserSerializerForOutput, SocialSerializer
from main.services.team.selectors import get_team_by_owner
from main.services.user.selectors import get_app_user_by_email, get_app_user_by_id


class TeamWorkerSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True, source='project')

    name = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
        source='project'
    )

    roleId = serializers.PrimaryKeyRelatedField(read_only=True, source='role')

    roleName = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
        source='role'
    )

    roleColor = serializers.SlugRelatedField(
        read_only=True,
        slug_field='color',
        source='role'
    )

    class Meta:
        model = ProjectEmployee
        fields = ('id', 'name', 'roleId', 'roleName', 'roleColor')


class TeammateSerializerForAdd(UserSerializerForOutput):
    name = serializers.CharField()
    email = serializers.EmailField()
    authority = serializers.IntegerField(read_only=True)
    social = SocialSerializer(many=True, source='socials', read_only=True)

    def create(self, validated_data, *args, **kwargs):
        team_owner_id = validated_data['team_owner_id']
        team_owner = get_app_user_by_id(id=team_owner_id)
        email = validated_data['email']
        name = validated_data['name']

        team = get_team_by_owner(owner=team_owner)
        user_to_add = get_app_user_by_email(email=email)

        if user_to_add:
            if user_to_add.id not in team.participants.values_list('id', flat=True):
                team.participants.add(user_to_add)

        else:
            user_to_add = AppUser.objects.create(name=name, email=email, is_register=False, authority=0)
            team.participants.add(user_to_add)

        return user_to_add


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
