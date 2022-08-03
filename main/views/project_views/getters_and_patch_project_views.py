from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from main.const_data.template_errors import *
from main.pagination import ProjectPagination
from main.parsers import *
from main.serializers.project_serializers.project_serializers import ProjectSerializerLong, ProjectSerializerShort
from main.services.project.selectors import get_projects_by_owner
from main.services.user.selectors import get_app_user_by_token


class ProjectsListAPIView(ListAPIView):
    serializer_class = ProjectSerializerLong

    def list(self, request, *args, **kwargs):
        user = get_app_user_by_token(token=get_token(request))
        if user:
            if request.headers.get('short', None) == 'true':
                self.serializer_class = ProjectSerializerShort

            paginate = request.headers.get('paginate', None)
            if paginate is not None:
                self.pagination_class = ProjectPagination

            flag_archived = request.headers.get('isArchived', 'false')
            queryset = get_projects_by_owner(owner_project=user, archived=flag_archived)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            output_data = {'projects': serializer.data} if paginate is None else serializer.data
            return Response(output_data, status=status.HTTP_200_OK)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)


class ProjectView(RetrieveUpdateAPIView):
    serializer_class = ProjectSerializerLong

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def retrieve(self, request, *args, **kwargs):
        user = get_app_user_by_token(token=get_token(request))
        if user:
            self.queryset = get_projects_by_owner(owner_project=user)
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, *args, **kwargs):
        user = get_app_user_by_token(token=get_token(request))
        if user:
            self.queryset = get_projects_by_owner(owner_project=user)
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)

            serializer.save(roles=request.data.get('roles', None))

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return Response(serializer.data)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)
