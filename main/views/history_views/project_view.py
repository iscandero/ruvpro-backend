from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from main.authentication import AppUserAuthentication
from main.const_data.template_errors import USER_NOT_FOUND_DATA
from main.pagination import HistoryPagination
from main.serializers.history_serializers import TimeEntrySerializerForHistory, AdvanceSerializerForHistory
from main.serializers.statistics_serializers.projects_serializers import ProjectSerializerForStatistics
from main.services.advance.selectors import get_advances_by_user_and_project_id
from main.services.time_entry.selectors import get_time_entrys_by_user_and_project_id
from main.services.worker.selectors import get_workers_by_user
from itertools import chain


class ProjectHistoryListAPIView(ListAPIView):
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
            return Response({'projectsHistory': serializer.data})

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)


class AdvanceWorkTimeHistoryListAPIView(ListAPIView):
    authentication_classes = [AppUserAuthentication]
    serializer_class = TimeEntrySerializerForHistory

    def list(self, request, *args, **kwargs):
        user = request.user
        if user:
            project_id = kwargs['pk']
            paginate = request.headers.get('paginate', None)

            time_entrys = get_time_entrys_by_user_and_project_id(user, project_id)

            dates_list = time_entrys.values_list('date', flat=True)
            advances = get_advances_by_user_and_project_id(user, project_id).exclude(date__in=dates_list)

            queryset = time_entrys

            if paginate is not None:
                self.pagination_class = HistoryPagination

            page = self.paginate_queryset(list(chain(queryset, advances)))
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                data = serializer.data + AdvanceSerializerForHistory(advances, many=True).data
                return self.get_paginated_response(data)

            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data + AdvanceSerializerForHistory(advances, many=True).data
            return Response(data, status=status.HTTP_200_OK)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)