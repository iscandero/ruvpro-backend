from rest_framework import serializers

from main.models import FileUser
from main.services.user.selectors import get_all_users


class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField(use_url=True)
    user = serializers.PrimaryKeyRelatedField(write_only=True, queryset=get_all_users())

    class Meta:
        model = FileUser
        fields = ('file', 'user')
