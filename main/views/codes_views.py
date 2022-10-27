from rest_framework.generics import ListAPIView

from main.serializers.codes_serializers import CodeRoleSerializer
from main.services.codes.selectors import get_all_role_codes


class CodeRoleListAPIView(ListAPIView):
    serializer_class = CodeRoleSerializer
    queryset = get_all_role_codes()
