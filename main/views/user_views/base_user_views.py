from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from main.authentication import AppUserAuthentication
from main.const_data.template_errors import *
from main.serializers.user_serializers.user_serializers import UserSerializerForOutput, UserSerializerForUpdate
from main.services.auth.use_cases import delete_all_tokens_by_user


class UserView(APIView):
    authentication_classes = [AppUserAuthentication]

    def get(self, request):
        need_user = request.user
        if need_user:
            return Response(
                UserSerializerForOutput(need_user, context={'request': request, 'userId': need_user.id}).data,
                status=status.HTTP_200_OK)
        else:
            return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        need_user = request.user
        if need_user:
            serializer = UserSerializerForUpdate(data=request.data, instance=need_user)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                UserSerializerForOutput(need_user, context={'request': request, 'userId': need_user.id}).data,
                status=status.HTTP_200_OK)
        else:
            return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        need_user = request.user
        if need_user:
            need_user.is_deleted = True
            need_user.avatar = None
            need_user.bio = None
            need_user.socials.all().delete()
            need_user.save()
            delete_all_tokens_by_user(user=need_user)
            return Response(SUCCESS_DATA, status=status.HTTP_200_OK)

        else:
            return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)
