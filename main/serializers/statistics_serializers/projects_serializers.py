from rest_framework import serializers

from main.models import ProjectEmployee


class ProjectSerializerForStatistics(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(source='project', read_only=True)
    name = serializers.SlugRelatedField(source='project', slug_field='name', read_only=True)
    roleId = serializers.PrimaryKeyRelatedField(source='role', read_only=True)
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
    totalSalary = serializers.SerializerMethodField('get_total_salary')
    totalWorkTime = serializers.SerializerMethodField('get_total_work_time')
    averageRate = serializers.FloatField(source='rate')
    currency = serializers.SlugRelatedField(source='project', slug_field='currency', read_only=True)

    class Meta:
        model = ProjectEmployee
        fields = ('id', 'name', 'roleId', 'roleName', 'roleColor', 'roleAmount', 'rolePercentage', 'totalSalary',
                  'totalWorkTime', 'averageRate', 'currency')

    def get_total_salary(self, instance):
        return instance.rate * instance.work_time

    def get_total_work_time(self, instance):
        return instance.work_time * 3600
