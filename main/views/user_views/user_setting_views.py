import json

from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from main.const_data.template_errors import *

from main.parsers import *
from main.serializers.user_serializers import RoleSerializer, UserSerializer
from main.services.role.base_role.selectors import get_all_base_roles_by_author

from main.services.role.selectors import get_role_by_id
from main.services.user.selectors import get_app_user_by_token


@method_decorator(csrf_exempt, name='dispatch')
class UserSettingsCurrencyView(APIView):
    def put(self, request):
        token = get_token(request)
        need_user = get_app_user_by_token(token=token)

        if need_user:
            serializer = UserSerializer(data=request.data, instance=need_user)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(SUCCESS_DATA, status=200)

        else:
            return Response(USER_NOT_FOUND_DATA, status=401)


class SettingsAPIView(APIView):
    def get(self, request):
        token = get_token(request)
        need_user = get_app_user_by_token(token=token)
        if need_user:
            roles = get_all_base_roles_by_author(author=need_user)
            return Response({"roles": RoleSerializer(roles, many=True).data, "currency": need_user.currency})

        else:
            return Response(USER_NOT_FOUND_DATA, status=401)

    def post(self, request):
        token = get_token(request)
        need_user = get_app_user_by_token(token=token)
        if need_user:
            request.data['author_id'] = need_user.id
            serializer = RoleSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        else:
            return Response(USER_NOT_FOUND_DATA, status=401)


class UserViewForIndexInEnd(APIView):
    def patch(self, request, role_id):
        token = get_token(request)

        user = get_app_user_by_token(token=token)
        if user:
            try:
                role = get_role_by_id(role_id=role_id)
            except:
                return Response(ROLE_NOT_FOUND_DATA, status=404)
            serializer = RoleSerializer(data=request.data, instance=role)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(USER_NOT_FOUND_DATA, status=401)

    def delete(self, request, role_id):
        token = get_token(request)
        user = get_app_user_by_token(token=token)

        if user:
            try:
                role_to_delete = get_role_by_id(role_id=role_id)
            except:
                return Response(ROLE_NOT_FOUND_DATA, status=404)

            if role_to_delete.author == user:
                role_to_delete.delete()
                return Response(DELETE_SUCCESS_DATA, status=200)
            else:
                return Response(NO_PERMISSION_DATA, status=404)
        else:
            return Response(USER_NOT_FOUND_DATA, status=401)
