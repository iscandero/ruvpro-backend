from rest_framework.response import Response
from rest_framework.views import APIView
from main.authentication import AppUserAuthentication
from main.const_data.template_errors import *
from main.serializers.user_serializers.user_serializers import RoleSerializer, CurrencyUserSerializer
from main.services.role.base_role.selectors import get_all_base_roles_by_author
from main.services.role.selectors import get_role_by_id
from rest_framework import status


class UserSettingsCurrencyView(APIView):
    authentication_classes = [AppUserAuthentication]

    def put(self, request):
        need_user = request.user

        if need_user:
            serializer = CurrencyUserSerializer(data=request.data, instance=need_user)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(SUCCESS_DATA, status=status.HTTP_200_OK)

        else:
            return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)


class SettingsAPIView(APIView):
    authentication_classes = [AppUserAuthentication]

    def get(self, request):
        need_user = request.user
        if need_user:
            roles = get_all_base_roles_by_author(author=need_user)
            return Response({"roles": RoleSerializer(roles, many=True).data, "currency": need_user.currency},
                            status=status.HTTP_200_OK)

        else:
            return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        need_user = request.user
        if need_user:
            request.data['author_id'] = need_user.id
            serializer = RoleSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)


class UserViewForIndexInEnd(APIView):
    authentication_classes = [AppUserAuthentication]

    def patch(self, request, role_id):
        user = request.user
        if user:
            try:
                role = get_role_by_id(role_id=role_id)
            except:
                return Response(ROLE_NOT_FOUND_DATA, status=status.HTTP_400_BAD_REQUEST)
            serializer = RoleSerializer(data=request.data, instance=role)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, role_id):
        user = request.user
        if user:
            try:
                role_to_delete = get_role_by_id(role_id=role_id)
            except:
                return Response(ROLE_NOT_FOUND_DATA, status=status.HTTP_400_BAD_REQUEST)

            if role_to_delete.author == user:
                role_to_delete.delete()
                return Response(DELETE_SUCCESS_DATA, status=status.HTTP_200_OK)
            else:
                return Response(NO_PERMISSION_DATA, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)
