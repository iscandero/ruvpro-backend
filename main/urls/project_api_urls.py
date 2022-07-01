from django.urls import path

from main.views.project_views import base_project_views, getters_project_views, worker_views

urlpatterns = [
    path('api/project', base_project_views.ProjectView.as_view()),
    path('api/project/<int:project>/time-entry', worker_views.TimeEntryView.as_view()),
    path('api/workers/<int:worker_id>', worker_views.WorkerViewWithIndexInEnd.as_view()),
    path('api/project/<int:project>/worker', worker_views.AddWorkerView.as_view()),
    path('api/projects/paginate', getters_project_views.GetProjectsWithPaginateView.as_view()),
    path('api/projects', getters_project_views.GetProjectsView.as_view()),
    path('api/project/<int:project>/set-complete', base_project_views.SetCompleteProjectView.as_view()),
    path('api/project/<int:project>', getters_project_views.GetProjectView.as_view()),
    path('api/project/advance', worker_views.AdvanceView.as_view()),
]
