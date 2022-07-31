from rest_framework import serializers

from main.models import ProjectEmployee, Role
from main.services.role.selectors import get_all_project_roles, get_role_by_id
from main.services.worker.use_cases import get_rate_by_worker


class ImageUrlField(serializers.RelatedField):
    def to_representation(self, instance):
        if instance.avatar:
            url = instance.avatar.url
        else:
            return None

        request = self.context.get('request', None)
        return request.build_absolute_uri(url)


class WorkerSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(read_only=True, source='user')
    rate = serializers.SerializerMethodField()
    avatar = ImageUrlField(read_only=True, source='user')
    roleId = serializers.PrimaryKeyRelatedField(source='role',
                                                queryset=get_all_project_roles())
    workTime = serializers.SerializerMethodField()
    name = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
        source='user'
    )
    projectId = serializers.PrimaryKeyRelatedField(read_only=True, source='project')
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
    roleAmount = serializers.SlugRelatedField(
        read_only=True,
        slug_field='amount',
        source='role'
    )
    rolePercentage = serializers.SlugRelatedField(
        read_only=True,
        slug_field='percentage',
        source='role'
    )

    def get_rate(self, instance):
        return get_rate_by_worker(worker=instance)

    def get_workTime(self, instance):
        return instance.work_time * 3600

    class Meta:
        model = ProjectEmployee
        fields = ('id', 'userId', 'rate', 'roleId', 'workTime', 'avatar', 'name', 'projectId',
                  'roleName', 'roleColor', 'roleAmount', 'rolePercentage',)
        read_only_fields = ('advance', 'salary')

    def update(self, instance, validated_data):
        instance.role = validated_data.get('role')
        instance.save(update_fields=['role'])
        return instance
