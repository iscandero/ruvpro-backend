from rest_framework import status
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from main.authentication import AppUserAuthentication
from main.const_data.template_errors import *
from main.parsers import *
from main.serializers.project_serializers.work_time_serializers import WorkTimeSerializer, WorkTimeSerializerForOutput
from main.serializers.project_serializers.worker_serializers import WorkerSerializer, WorkerSerializerToCreate
from main.serializers.project_serializers.advance_serializer import AdvanceSerializer
from main.services.advance.selectors import get_advance_by_date_and_worker_id, get_advance_by_date_and_project_id
from main.services.project.selectors import get_project_by_id
from main.services.time_entry.selectors import get_time_entry_by_date_and_worker_id, \
    get_time_entry_by_date_and_project_id
from main.services.user.selectors import get_app_user_by_token
from main.services.work_with_date import convert_timestamp_to_date
from main.services.worker.selectors import get_worker_by_id, get_all_workers


class UpdateDestroyAPIViewWorkerAPIView(UpdateAPIView, DestroyAPIView):
    queryset = get_all_workers()
    serializer_class = WorkerSerializer
    authentication_classes = [AppUserAuthentication]

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user:
            worker_id = kwargs.get('pk')
            worker = get_worker_by_id(worker_id=worker_id)
            instance = self.get_object()
            if worker.project.owner == user:
                self.perform_destroy(instance)
                return Response(DELETE_SUCCESS_DATA, status=status.HTTP_200_OK)
            else:
                return Response(NO_PERMISSION_DATA, status=status.HTTP_403_FORBIDDEN)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def patch(self, request, *args, **kwargs):
        user = request.user
        if user:
            worker_id = kwargs.get('pk')
            worker = get_worker_by_id(worker_id=worker_id)
            if worker.project.owner == user:
                return self.partial_update(request, *args, **kwargs)

            else:
                return Response(NO_PERMISSION_DATA, status=status.HTTP_403_FORBIDDEN)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)


class AddWorkerAPIView(APIView):
    authentication_classes = [AppUserAuthentication]

    def post(self, request, project_id):
        user = request.user
        if user:
            try:
                project = get_project_by_id(project_id=project_id)
            except:
                return Response(PROJECT_NOT_FOUND_DATA, status=status.HTTP_400_BAD_REQUEST)

            if project.owner == user:
                serializer = WorkerSerializerToCreate(data=request.data)
                serializer.is_valid(raise_exception=True)

                return Response(WorkerSerializer(serializer.save(project=project), context={'request': request}).data,
                                status=status.HTTP_201_CREATED)
            else:
                Response(NO_PERMISSION_DATA, status=status.HTTP_403_FORBIDDEN)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)


class AdvanceCreateAPIView(APIView):
    authentication_classes = [AppUserAuthentication]
    def get(self, request):
        user = request.user
        if user:
            timestamp = float(request.headers['date'])
            date = convert_timestamp_to_date(timestamp=timestamp)
            worker_id = request.headers.get('workerId', None)
            project_id = request.headers.get('projectId', None)
            if worker_id is not None:
                queryset = get_advance_by_date_and_worker_id(worker_id=int(worker_id), date=date)
                return Response(AdvanceSerializer(queryset).data, status=status.HTTP_200_OK)

            if project_id is not None:
                queryset = get_advance_by_date_and_project_id(project_id=int(project_id), date=date)
                return Response({'times': AdvanceSerializer(queryset, many=True).data},
                                status=status.HTTP_200_OK)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, *args, **kwargs):
        user = request.user
        if user:
            times = request.data['times']
            serializer = AdvanceSerializer(data=times, many=True)
            serializer.is_valid(raise_exception=True)
            workers_to_output = serializer.save(times=times, initiator=user)

            return Response(
                {'workers': WorkerSerializer(workers_to_output, context={'request': request}, many=True).data},
                status=status.HTTP_201_CREATED)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)


class TimeEntryGetCreateAPIView(APIView):
    authentication_classes = [AppUserAuthentication]

    def post(self, request, *args, **kwargs):
        user = request.user
        if user:
            times = request.data['times']
            serializer = WorkTimeSerializer(data=times, many=True)
            serializer.is_valid(raise_exception=True)
            workers_to_output = serializer.save(times=times, initiator=user)

            return Response(
                {'workers': WorkerSerializer(workers_to_output, context={'request': request}, many=True).data},
                status=status.HTTP_201_CREATED)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        user = request.user
        if user:
            timestamp = float(request.headers['date'])
            date = convert_timestamp_to_date(timestamp=timestamp)
            worker_id = request.headers.get('workerId', None)
            project_id = request.headers.get('projectId', None)
            if worker_id is not None:
                queryset = get_time_entry_by_date_and_worker_id(worker_id=int(worker_id), date=date)
                return Response(WorkTimeSerializerForOutput(queryset).data, status=status.HTTP_200_OK)

            if project_id is not None:
                queryset = get_time_entry_by_date_and_project_id(project_id=int(project_id), date=date)
                return Response({'times': WorkTimeSerializerForOutput(queryset, many=True).data},
                                status=status.HTTP_200_OK)

        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)
