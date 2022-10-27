from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from main.authentication import AppUserAuthentication
from main.const_data.template_errors import *
from main.pagination import ProjectPagination
from main.serializers.project_serializers.project_serializers import ProjectSerializerLong, ProjectSerializerShort
from main.services.project.selectors import get_projects_for_owner_or_member


class ProjectsListAPIView(ListAPIView):
    serializer_class = ProjectSerializerLong
    authentication_classes = [AppUserAuthentication]

    def list(self, request, *args, **kwargs):
        user = request.user
        if user:
            if request.headers.get('short', None) == 'true':
                self.serializer_class = ProjectSerializerShort

            paginate = request.headers.get('paginate', None)
            if paginate is not None:
                self.pagination_class = ProjectPagination

            flag_archived = request.headers.get('isArchived', 'false')
            queryset = get_projects_for_owner_or_member(viewer_user=user, archived=flag_archived)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, context={'user_id': user.id}, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, context={'user_id': user.id}, many=True)
            output_data = {'projects': serializer.data} if paginate is None else serializer.data
            return Response(output_data, status=status.HTTP_200_OK)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)


class ProjectView(RetrieveUpdateAPIView):
    serializer_class = ProjectSerializerLong
    authentication_classes = [AppUserAuthentication]

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        if user:
            self.queryset = get_projects_for_owner_or_member(viewer_user=user)
            instance = self.get_object()
            serializer = self.get_serializer(instance, context={'user_id': user.id})
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        user = request.user
        if user:
            self.queryset = get_projects_for_owner_or_member(viewer_user=user)
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, context={'user_id': user.id}, partial=partial)
            serializer.is_valid(raise_exception=True)

            serializer.save(roles=request.data.get('roles', None))

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)
