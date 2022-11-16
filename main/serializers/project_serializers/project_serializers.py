from rest_framework import serializers

from main.models import Project
from main.serializers.project_serializers.worker_serializers import WorkerSerializer
from main.serializers.user_serializers.user_serializers import RoleSerializer
from main.services.history_work_time_project.interactors import write_project_time_entry_to_history_table
from main.services.history_work_time_project.use_cases import get_difference_project_work_time
from main.services.role.selectors import get_role_by_id


class ProjectSerializerLong(serializers.ModelSerializer):
    workers = WorkerSerializer(many=True, read_only=True)
    roles = RoleSerializer(many=True)
    isArchived = serializers.BooleanField(source='is_archived', required=False)
    percentMasterByStudent = serializers.FloatField(required=False)
    percentMentorByStudent = serializers.FloatField(required=False)
    workTime = serializers.SerializerMethodField()
    averageRate = serializers.FloatField(source='average_rate')
    differenceTimeEntry = serializers.SerializerMethodField()
    isEditable = serializers.SerializerMethodField('get_is_editable')

    class Meta:
        model = Project
        fields = ('id', 'name', 'workers', 'roles', 'budget', 'isArchived', 'workTime', 'averageRate', 'currency',
                  'differenceTimeEntry', 'isEditable', 'percentMasterByStudent', 'percentMentorByStudent')

    def get_differenceTimeEntry(self, instance):
        difference = get_difference_project_work_time(project=instance)
        write_project_time_entry_to_history_table(project=instance)
        return difference

    def get_is_editable(self, instance):
        return True if instance.owner.id == self.context.get('user_id') else False

    def update(self, instance, validated_data):
        update_fields = []
        budget = validated_data.get('budget', None)
        if budget is not None:
            instance.budget = budget
            instance.save(update_fields=['budget'])

        name = validated_data.get('name', None)
        if name is not None:
            instance.name = name
            update_fields.append('name')

        currency = validated_data.get('currency', None)
        if currency is not None:
            instance.currency = currency
            update_fields.append('currency')

        percent_master_by_student = validated_data.get('percentMasterByStudent', None)
        if percent_master_by_student is not None:
            instance.percentMasterByStudent = percent_master_by_student
            update_fields.append('percentMasterByStudent')
        percent_mentor_by_student = validated_data.get('percentMentorByStudent', None)
        if percent_mentor_by_student is not None:
            instance.percentMentorByStudent = percent_mentor_by_student
            update_fields.append('percentMentorByStudent')

        instance.save(update_fields=update_fields)

        roles = validated_data.get('roles', None)

        if roles is not None:
            for role in roles:
                role_id = role.get('id')
                role_instance = get_role_by_id(role_id)
                serializer = RoleSerializer(data=role, instance=role_instance)
                serializer.is_valid(raise_exception=True)
                serializer.save()



        return instance

    def get_workTime(self, instance):
        return instance.work_time * 3600


class ProjectSerializerShort(serializers.ModelSerializer):
    isArchived = serializers.BooleanField(source='is_archived')
    isEditable = serializers.SerializerMethodField('get_is_editable')

    class Meta:
        model = Project
        fields = ('id', 'name', 'isArchived', 'isEditable')

    def get_is_editable(self, instance):
        return True if instance.owner.id == self.context.get('user_id') else False


class ProjectSetCompleteSerializer(serializers.ModelSerializer):
    isArchived = serializers.BooleanField(source='is_archived')

    class Meta:
        model = Project
        fields = ('isArchived',)
