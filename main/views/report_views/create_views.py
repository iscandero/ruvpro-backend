from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from main.authentication import AppUserAuthentication
from main.const_data.template_errors import USER_NOT_FOUND_DATA
from main.serializers.report.model_serializer import ModelReportSerializer
from main.services.report.interactors import create_report_object_by_user_and_project


class CreateReport(CreateAPIView):
    serializer_class = ModelReportSerializer
    authentication_classes = [AppUserAuthentication]

    def create(self, request, *args, **kwargs):
        user = request.user
        if user:
            project_id = kwargs['pk']
            report = create_report_object_by_user_and_project(user, project_id)
            serializer = self.get_serializer(report)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(USER_NOT_FOUND_DATA, status=status.HTTP_401_UNAUTHORIZED)


