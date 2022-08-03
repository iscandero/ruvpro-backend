from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from main.authentication import AppUserAuthentication
from main.const_data.template_errors import USER_NOT_FOUND_DATA
from main.serializers.team_serializers import TeammateSerializerForAdd


class AddUserToTeam(APIView):
    authentication_classes = [AppUserAuthentication]

    def post(self, request):
        user = request.user
        if user:
            serializer = TeammateSerializerForAdd(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save(team_owner_id=user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)
