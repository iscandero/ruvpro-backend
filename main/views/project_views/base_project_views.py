from rest_framework import status
from rest_framework.generics import UpdateAPIView, CreateAPIView
from rest_framework.response import Response

from main.authentication import AppUserAuthentication
from main.const_data.template_errors import *

from main.parsers import *
from main.serializers.project_serializers.create_serializers import ProjectSerializerForCreate
from main.serializers.project_serializers.project_serializers import ProjectSetCompleteSerializer, ProjectSerializerLong
from main.services.project.selectors import get_projects_for_owner_or_member, get_all_project
from main.services.user.selectors import get_app_user_by_token


class SetCompleteProjectView(UpdateAPIView):
    serializer_class = ProjectSetCompleteSerializer
    authentication_classes = [AppUserAuthentication]

    def patch(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        user = request.user
        if user:
            self.queryset = get_projects_for_owner_or_member(viewer_user=user)
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response(SUCCESS_DATA, status=status.HTTP_200_OK)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)


class ProjectCreateAPIView(CreateAPIView):
    serializer_class = ProjectSerializerForCreate
    authentication_classes = [AppUserAuthentication]
    queryset = get_all_project()

    def create(self, request, *args, **kwargs):
        user = request.user
        if user:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            project = serializer.save(owner=user)
            return Response(ProjectSerializerLong(project, context={'user_id': user.id}).data,
                            status=status.HTTP_201_CREATED)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)
