from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from main.authentication import AppUserAuthentication
from main.const_data.template_errors import USER_NOT_FOUND_DATA
from main.serializers.statistics_serializers.projects_serializers import ProjectSerializerForStatistics
from main.services.worker.selectors import get_workers_by_user


class GetProjectStatistic(ListAPIView):
    authentication_classes = [AppUserAuthentication]
    serializer_class = ProjectSerializerForStatistics

    def list(self, request, *args, **kwargs):
        user = request.user
        if user:
            queryset = get_workers_by_user(user=user)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response({'projectsStatistics': serializer.data})

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)
