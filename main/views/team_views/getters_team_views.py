from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from main.authentication import AppUserAuthentication
from main.const_data.template_errors import *
from main.serializers.team_serializers import TeamWorkerSerializer
from main.serializers.user_serializers.user_serializers import UserSerializerForOutput
from main.services.team.selectors import get_team_by_owner
from main.services.user.selectors import get_app_user_by_id
from main.services.worker.selectors import get_workers_by_user_and_willing


class GetUsersByTeam(ListAPIView):
    serializer_class = UserSerializerForOutput
    authentication_classes = [AppUserAuthentication]

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, context={'userId': user.id}, many=True)
        if 'projects' in request.headers:
            for teammate in serializer.data:
                user_id = get_app_user_by_id(id=teammate['id'])
                teammate['projects'] = TeamWorkerSerializer(
                    get_workers_by_user_and_willing(user=user_id, willing=user), many=True).data

        return Response({'teammates': serializer.data}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        user = request.user
        if user:
            self.queryset = get_team_by_owner(owner=user).participants
            return self.list(request, *args, **kwargs)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)


class GetProjectsByTeamUser(ListAPIView):
    serializer_class = TeamWorkerSerializer
    authentication_classes = [AppUserAuthentication]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response({'projects': serializer.data}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        user = request.user
        if user:
            user_id = kwargs.get('user_id', None)
            need_user = get_app_user_by_id(id=user_id)
            self.queryset = get_workers_by_user_and_willing(user=need_user, willing=user)
            return self.list(request, *args, **kwargs)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)
