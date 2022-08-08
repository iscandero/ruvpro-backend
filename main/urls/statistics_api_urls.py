from django.urls import path

from main.views.statistics_views import worker_view, advance_view, project_view

urlpatterns = [
    path('api/statistics/personal', worker_view.AllWorkerStatisticAPIView.as_view()),
    path('api/statistics/personal/projects', project_view.ProjectStatisticListAPIView.as_view()),
    path('api/statistics/personal/projects/<int:pk>', project_view.ProjectsStatisticAPIView.as_view()),
    path('api/statistics/personal/projects/<int:pk>/worker', worker_view.WorkerStatisticAPIView.as_view()),
]
