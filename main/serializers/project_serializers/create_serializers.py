from rest_framework import serializers

from main.models import Project, ProjectEmployee, Role
from main.services.codes.selectors import get_code_by_role_name
from main.services.role.project_role.selectors import get_role_by_name_and_project
from main.services.user.selectors import get_all_users


class RoleSerializerForCreateProject(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('name', 'description', 'color', 'percentage', 'amount', 'type')

    def create(self, validated_data):
        validated_data['code'] = get_code_by_role_name(name=validated_data['name'])
        return Role.objects.create(**validated_data)


class WorkerSerializerForCreateProject(serializers.ModelSerializer):
    userId = serializers.PrimaryKeyRelatedField(queryset=get_all_users(), source='user', required=False)
    roleName = serializers.CharField()

    class Meta:
        model = ProjectEmployee
        fields = ('userId', 'roleName')

    def create(self, validated_data):
        project = validated_data.get('project', None)
        role_name = validated_data.get('roleName', None)
        user = validated_data.get('user', None)
        role = get_role_by_name_and_project(name=role_name, project=project)
        return ProjectEmployee.objects.create(user=user, role=role, project=project)


class ProjectSerializerForCreate(serializers.ModelSerializer):
    roles = RoleSerializerForCreateProject(many=True)
    workers = WorkerSerializerForCreateProject(many=True, required=False)

    class Meta:
        model = Project
        fields = ('name', 'budget', 'roles', 'workers', 'currency')

    def create(self, validated_data):
        name = validated_data.get('name', None)
        budget = validated_data.get('budget', None)
        currency = validated_data.get('currency', None)
        owner = validated_data.get('owner', None)
        project = Project.objects.create(name=name, budget=budget, owner=owner, is_archived=False, currency=currency)

        roles = validated_data.get('roles', None)
        serializer = RoleSerializerForCreateProject(data=roles, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=owner, project=project)

        workers = validated_data.get('workers', None)
        if workers is not None:
            for worker in workers:
                serializer = WorkerSerializerForCreateProject(data=worker)
                serializer.is_valid(raise_exception=True)
                serializer.save(project=project, user=worker['user'])
        return project
