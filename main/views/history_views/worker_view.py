from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from main.authentication import AppUserAuthentication
from main.const_data.template_errors import USER_NOT_FOUND_DATA, WORKER_NOT_FOUND
from main.serializers.history_serializers import WorkerSerializerForHistory
from main.services.worker.selectors import get_worker_by_user_and_project_id


class WorkerHistoryAPIView(APIView):
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


