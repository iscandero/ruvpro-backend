from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.authentication import AppUserAuthentication
from main.const_data.template_errors import *
from main.services.team.selectors import get_team_by_owner
from main.services.user.selectors import get_app_user_by_id


class DeleteUserByTeam(APIView):
    authentication_classes = [AppUserAuthentication]

    def delete(self, request, user_id):
        user = request.user
        if user:
            user_to_delete_from_team = get_app_user_by_id(id=user_id)
            team = get_team_by_owner(owner=user)
            team.participants.remove(user_to_delete_from_team)
            return Response(DELETE_SUCCESS_DATA, status=status.HTTP_200_OK)
        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)
