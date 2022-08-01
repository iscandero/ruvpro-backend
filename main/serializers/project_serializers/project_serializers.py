from rest_framework import serializers

from main.models import Project
from main.serializers.project_serializers.worker_serializers import WorkerSerializer
from main.serializers.user_serializers import RoleSerializer
from main.services.history_work_time_project.interactors import write_project_time_entry_to_history_table
from main.services.history_work_time_project.use_cases import get_difference_project_work_time


class ProjectSerializer(serializers.ModelSerializer):
    workers = WorkerSerializer(many=True, read_only=True)
    roles = RoleSerializer(many=True, read_only=True)
    isArchived = serializers.BooleanField(source='is_archived')
    workTime = serializers.FloatField(source='work_time')
    averageRate = serializers.FloatField(source='average_rate')
    differenceTimeEntry = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'workers', 'roles', 'budget', 'isArchived', 'workTime', 'averageRate', 'currency',
                  'differenceTimeEntry')

    def get_differenceTimeEntry(self, instance):
        difference = get_difference_project_work_time(project=instance)
        write_project_time_entry_to_history_table(project=instance)
        return difference
