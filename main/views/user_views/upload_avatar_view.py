from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from main.authentication import AppUserAuthentication
from main.const_data.template_errors import USER_NOT_FOUND_DATA
from main.serializers.user_serializers.user_avatar_serializers import FileSerializer
from main.services.user.selectors import get_all_files


class UploadFile(CreateAPIView):
    serializer_class = FileSerializer
    queryset = get_all_files()
    authentication_classes = [AppUserAuthentication]

    def create(self, request, *args, **kwargs):
        user = request.user
        if user:
            request.data['user'] = user.id
            serializer = self.get_serializer(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)


