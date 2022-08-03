from rest_framework import serializers

from main.models import FileUser
from main.services.user.selectors import get_all_users


class FileSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(use_url=False)
    baseURL = serializers.SerializerMethodField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(write_only=True, queryset=get_all_users())

    class Meta:
        model = FileUser
        fields = ('file', 'baseURL', 'user')

    def get_baseURL(self, data):
        request = self.context.get('request')
        return str(request.build_absolute_uri('/')) + 'media/'
