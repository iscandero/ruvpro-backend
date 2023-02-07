from django.urls import path

from main.views.history_views import worker_view, project_view

urlpatterns = [
    path('api/history/projects', project_view.ProjectHistoryListAPIView.as_view()),
    path('api/history/projects/<int:pk>/worker', worker_view.WorkerHistoryAPIView.as_view()),
    path('api/history/personal/projects/<int:pk>', project_view.AdvanceWorkTimeHistoryListAPIView.as_view()),
]
