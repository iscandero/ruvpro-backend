from django.urls import path

from main.views.report_views.create_views import CreateForSimpleUserReport, CreateForMultiUsersReport

urlpatterns = [
    path('api/report/personal/projects/<int:pk>', CreateForSimpleUserReport.as_view()),
    path('api/report/personal/projects', CreateForSimpleUserReport.as_view()),
    path('api/report/projects/<int:pk>', CreateForMultiUsersReport.as_view()),
]

