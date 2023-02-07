from rest_framework import serializers

from main.models import ProjectEmployee
from main.serializers.fields import TimestampField
from main.serializers.project_serializers.worker_serializers import ModelRoleSerializer
from main.services.advance.selectors import get_advance_by_date_and_worker
from main.services.time_entry.selectors import get_time_entry_by_date_and_worker_id
from main.services.time_entry.use_cases import get_count_workdays_by_worker


class WorkerSerializerForHistory(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(source='user', slug_field='name', read_only=True)
    avatar = serializers.SlugRelatedField(source='user', slug_field='avatar', read_only=True)
    totalSalary = serializers.FloatField(source='salary')
    role = ModelRoleSerializer()
    workdaysCount = serializers.SerializerMethodField('get_count_workdays')

    class Meta:
        model = ProjectEmployee
        fields = ('id', 'name', 'avatar', 'role', 'rate', 'workdaysCount', 'advance', 'totalSalary')

    def get_count_workdays(self, instance):
        return get_count_workdays_by_worker(worker=instance)


class TimeEntrySerializerForHistory(serializers.Serializer):
    projectId = serializers.SerializerMethodField('get_project_id')
    workTime = serializers.FloatField(source='work_time', read_only=True)
    date = TimestampField()
    advance = serializers.SerializerMethodField()
    salary = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'projectId',
            'workTime',
            'advance',
            'date',
            'salary',
            'currency',)

    def get_advance(self, instance):
        advance = get_advance_by_date_and_worker(instance.employee, instance.date).advance
        if advance == 0:
            advance = None

        return advance

    def get_project_id(self, instance):
        return instance.employee.project.id

    def get_salary(self, instance):
        percent_complete = instance.employee.project.percentComplete
        return instance.employee.rate * instance.work_time * percent_complete / 100

    def get_currency(self, instance):
        return instance.employee.project.currency


class AdvanceSerializerForHistory(serializers.Serializer):
    projectId = serializers.SerializerMethodField('get_project_id')
    advance = serializers.FloatField(read_only=True)
    date = TimestampField()
    workTime = serializers.SerializerMethodField('get_work_time')
    salary = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'projectId',
            'workTime',
            'advance',
            'date',
            'salary',
            'currency',)

    def get_work_time(self, instance):
        return None

    def get_salary(self, instance):
        return None

    def get_project_id(self, instance):
        return instance.employee.project.id

    def get_currency(self, instance):
        return instance.employee.project.currency
