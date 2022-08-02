from django.urls import path

from main.views.project_views import base_project_views, getters_and_patch_project_views, worker_views

urlpatterns = [
    path('api/project', base_project_views.ProjectView.as_view()),
    path('api/project/time-entry', worker_views.TimeEntryGetCreateAPIView.as_view()),
    path('api/workers/<int:pk>', worker_views.UpdateDestroyAPIViewWorkerAPIView.as_view()),
    path('api/project/<int:project_id>/worker', worker_views.AddWorkerAPIView.as_view()),
    path('api/projects', getters_and_patch_project_views.ProjectsListAPIView.as_view()),
    path('api/project/<int:pk>/set-complete', base_project_views.SetCompleteProjectView.as_view()),
    path('api/project/<int:pk>', getters_and_patch_project_views.ProjectView.as_view()),
    path('api/project/advance', worker_views.AdvanceCreateAPIView.as_view()),
]
