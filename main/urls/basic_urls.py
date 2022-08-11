from django.urls import path

from main.views.basic_views import main_views

urlpatterns = [
    path('', main_views.index),
    path('developer-helper', main_views.apis_info),
    path('api/generator-test-users-ruvpro', main_views.GeneratorTestUsersAPIView.as_view()),
    path('api/generator-test-projects-ruvpro', main_views.GeneratorTestProjectsAPIView.as_view()),
]
