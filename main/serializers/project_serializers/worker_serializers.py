from rest_framework import serializers

from main.models import ProjectEmployee, Role
from main.services.role.selectors import get_all_project_roles
from main.services.user.selectors import get_all_users


class ModelRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class WorkerSerializer(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(read_only=True, source='user')
    # avatar = ImageUrlField(read_only=True, source='user')
    avatar = serializers.SlugRelatedField(slug_field='avatar', source='user', read_only=True)
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

    def get_workTime(self, instance):
        return instance.work_time * 3600

    class Meta:
        model = ProjectEmployee
        fields = ('id', 'userId', 'rate', 'advance', 'salary', 'roleId', 'workTime', 'avatar', 'name', 'projectId',
                  'roleName', 'roleColor', 'roleAmount', 'rolePercentage',)

    def update(self, instance, validated_data):
        instance.role = validated_data.get('role')
        instance.save(update_fields=['role'])
        return instance


class WorkerSerializerToCreate(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(source='user', queryset=get_all_users())
    roleId = serializers.PrimaryKeyRelatedField(source='role',
                                                queryset=get_all_project_roles())

    class Meta:
        model = ProjectEmployee
        fields = ('userId', 'roleId')

    def create(self, validated_data):
        user = validated_data.get('user', None)
        role = validated_data.get('role', None)
        if user is not None and role is not None:
            project = validated_data.get('project')
            return ProjectEmployee.objects.create(user=user, role=role, project=project)
