import operator
from itertools import chain

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from main.authentication import AppUserAuthentication
from main.const_data.template_errors import USER_NOT_FOUND_DATA, WORKER_NOT_FOUND
from main.pagination import HistoryPagination
from main.serializers.history_serializers import WorkerSerializerForHistory, AdvanceTimeEntrySerializerForHistory
from main.services.advance.selectors import get_advances_by_user_and_project_id
from main.services.history.interactors import get_chain_advance_time_entry_queryset
from main.services.time_entry.selectors import get_time_entrys_by_user_and_project_id
from main.services.worker.selectors import get_worker_by_user_and_project_id, get_worker_by_id


class WorkerHistoryByProjectAPIView(APIView):
    authentication_classes = [AppUserAuthentication]

    def get(self, request, pk):
        user = request.user
        if user:
            try:
                worker = get_worker_by_user_and_project_id(user=user, project_id=pk)
            except:
                return Response(WORKER_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST)

            return Response(WorkerSerializerForHistory(worker).data, status=status.HTTP_200_OK)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)


class WorkerHistoryAPIView(APIView):
    authentication_classes = [AppUserAuthentication]

    def get(self, request, pk):
        user = request.user
        if user:
            try:
                worker = get_worker_by_id(pk)
            except:
                return Response(WORKER_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST)

            return Response(WorkerSerializerForHistory(worker).data, status=status.HTTP_200_OK)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)


class AdvanceWorkTimeWorkerHistoryListAPIView(ListAPIView):
    authentication_classes = [AppUserAuthentication]
    serializer_class = AdvanceTimeEntrySerializerForHistory

    def list(self, request, *args, **kwargs):
        user = request.user
        if user:
            try:
                worker_id = kwargs['pk']
                worker = get_worker_by_id(worker_id)
            except:
                return Response(WORKER_NOT_FOUND, status=status.HTTP_400_BAD_REQUEST)

            paginate = request.headers.get('paginate', None)

            if paginate is not None:
                self.pagination_class = HistoryPagination

            queryset = get_chain_advance_time_entry_queryset(worker.user, worker.project)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                data = serializer.data
                return self.get_paginated_response(data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)
