from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from main.const_data.template_errors import *
from main.parsers import *
from main.serializers.user_serializers.user_serializers import UserSerializerForOutput, UserSerializerForUpdate
from main.services.user.selectors import get_app_user_by_token


class UserView(APIView):
    def get(self, request):
        token = get_token(request)
        need_user = get_app_user_by_token(token=token)
        if need_user:
            return Response(UserSerializerForOutput(need_user, context={'request': request}).data,
                            status=status.HTTP_200_OK)
        else:
            return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        token = get_token(request)
        need_user = get_app_user_by_token(token=token)
        if need_user:
            serializer = UserSerializerForUpdate(data=request.data, instance=need_user)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(UserSerializerForOutput(need_user, context={'request': request}).data,
                            status=status.HTTP_200_OK)
        else:
            return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)
