from django.urls import path

from main.views.statistics_views import worker_view, advance_view, project_view

urlpatterns = [
    path('api/statistics/personal', worker_view.GetWorkerStatistic.as_view()),
    path('api/statistics/advances', advance_view.GetAdvanceStatistic.as_view()),
    path('api/statistics/projects', project_view.GetProjectStatistic.as_view()),
]
