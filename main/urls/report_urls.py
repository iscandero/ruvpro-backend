from django.urls import path

from main.views.report_views.create_views import CreateReport

urlpatterns = [
    path('api/report/project/<int:pk>', CreateReport.as_view()),
]

