from rest_framework import serializers

from main.models import HistoryAdvance
from main.serializers.fields import TimestampField
from main.services.advance.selectors import get_advance_by_date_and_worker
from main.services.worker.selectors import get_all_workers


class AdvanceSerializer(serializers.ModelSerializer):
    workerId = serializers.PrimaryKeyRelatedField(source='employee', queryset=get_all_workers())
    date = TimestampField()
    class Meta:
        model = HistoryAdvance
        fields = ('date', 'workerId', 'advance')

    def create(self, validated_data):
        worker = validated_data.get('employee')
        date = validated_data.get('date')
        advance = validated_data.get('advance')
        current_advance = get_advance_by_date_and_worker(worker=worker, date=date)
        if validated_data.get('initiator') == worker.project.owner:
            if current_advance:
                current_advance.advance = advance
                current_advance.save(update_fields=['advance'])
            else:
                HistoryAdvance.objects.create(employee=worker, date=date, advance=advance)

        return worker
