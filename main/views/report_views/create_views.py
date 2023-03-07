from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from main.authentication import AppUserAuthentication
from main.const_data.template_errors import USER_NOT_FOUND_DATA
from main.serializers.report.model_serializer import ModelReportSerializer
from main.services.report.use_cases import create_user_current_project_report, \
    create_current_project_report_for_all_workers


class CreateForSimpleUserReport(CreateAPIView):
    serializer_class = ModelReportSerializer
    authentication_classes = [AppUserAuthentication]

    def create(self, request, *args, **kwargs):
        user = request.user
        if user:
            project_id = kwargs.get('pk', None)
            from_date = request.headers.get('fromDate', None)
            to_date = request.headers.get('toDate', None)

            report = create_user_current_project_report(user, project_id, from_date, to_date)
            serializer = self.get_serializer(report)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)


class CreateForMultiUsersReport(CreateAPIView):
    serializer_class = ModelReportSerializer
    authentication_classes = [AppUserAuthentication]

    def create(self, request, *args, **kwargs):
        user = request.user
        if user:
            project_id = kwargs.get('pk', None)
            from_date = request.headers.get('fromDate', None)
            to_date = request.headers.get('toDate', None)

            report = create_current_project_report_for_all_workers(user, project_id, from_date, to_date)
            serializer = self.get_serializer(report)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)
