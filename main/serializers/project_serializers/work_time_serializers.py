from rest_framework import serializers
from main.models import TimeEntry
from main.serializers.fields import TimestampField
from main.services.time_entry.selectors import get_time_entry_by_date_and_worker
from main.services.worker.selectors import get_all_workers


class WorkTimeSerializer(serializers.ModelSerializer):
    workerId = serializers.PrimaryKeyRelatedField(source='employee', queryset=get_all_workers())
    workTime = serializers.FloatField(source='work_time')
    date = TimestampField()

    class Meta:
        model = TimeEntry
        fields = ('date', 'workerId', 'workTime')

    def create(self, validated_data):
        worker = validated_data.get('employee')
        date = validated_data.get('date')
        work_time = validated_data.get('work_time') / 3600
        initiator = validated_data.get('initiator')
        current_work_time = get_time_entry_by_date_and_worker(worker=worker, date=date)
        if initiator == worker.project.owner:
            if current_work_time:
                current_work_time.work_time = work_time
                current_work_time.save(update_fields=['work_time'])
            else:
                TimeEntry.objects.create(employee=worker, date=date, work_time=work_time, initiator=initiator)

        return worker


class WorkTimeSerializerForOutput(WorkTimeSerializer):
    workTime = serializers.SerializerMethodField()

    def get_workTime(self, instance):
        return instance.work_time * 3600
