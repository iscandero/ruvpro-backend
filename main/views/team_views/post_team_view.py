from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from main.const_data.template_errors import USER_NOT_FOUND_DATA
from main.parsers import get_token
from main.serializers.team_serializers import TeammateSerializerForAdd
from main.services.user.selectors import get_app_user_by_token


class AddUserToTeam(APIView):
    def post(self, request):
        token = get_token(request)
        user = get_app_user_by_token(token=token)
        if user:
            serializer = TeammateSerializerForAdd(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(team_owner_id=user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)
