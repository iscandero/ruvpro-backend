from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.authentication import AppUserAuthentication
from main.const_data.template_errors import USER_NOT_FOUND_DATA, NOT_UPDATE_USER
from main.serializers.user_serializers.user_serializers import UserSerializerForUpdate, UserSerializerForOutput
from main.services.user.selectors import get_app_user_by_id


class PatchTeammateView(APIView):
    authentication_classes = [AppUserAuthentication]

    def patch(self, request, user_id):
        user = request.user
        if user:
            user_for_update = get_app_user_by_id(user_id)
            if user_for_update.is_register and user_for_update != user:
                return Response(NOT_UPDATE_USER, status=status.HTTP_405_METHOD_NOT_ALLOWED)
            serializer = UserSerializerForUpdate(data=request.data, instance=user_for_update)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                UserSerializerForOutput(user_for_update, context={'request': request, 'userId': user.id}).data,
                status=status.HTTP_200_OK)
        else:
            return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)
