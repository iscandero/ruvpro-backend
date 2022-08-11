from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from main.authentication import AppUserAuthentication
from main.const_data.actual_urls import ACTUAL_URLS
from main.generate_test_data import create_test_users_and_owner_team, create_test_projects


def index(request):
    return render(request, 'main/index.html')


def apis_info(request):
    return render(request, 'main/apis-info.html', {'actual_urls': ACTUAL_URLS})


class GeneratorTestUsersAPIView(APIView):
    def post(self, request):
        create_test_users_and_owner_team()
        return Response(status=status.HTTP_200_OK)


class GeneratorTestProjectsAPIView(APIView):
    authentication_classes = [AppUserAuthentication]

    def post(self, request):
        owner = request.user
        create_test_projects(owner=owner)
        return Response(status=status.HTTP_200_OK)
