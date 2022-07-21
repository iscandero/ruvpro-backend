from django.urls import path

from main.views.basic_views import main_views

urlpatterns = [
    path('', main_views.index),
    path('developer-helper', main_views.apis_info)
]
