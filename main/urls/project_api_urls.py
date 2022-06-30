from django.urls import path

from main.views import projectViews

urlpatterns = [
    path('api/project', projectViews.ProjectView.as_view()),
    path('api/project/<int:project_id>/time-entry', projectViews.TimeEntryView.as_view()),
    path('api/workers/<int:worker_id>', projectViews.WorkerViewWithIndexInEnd.as_view()),
    path('api/project/<int:project_id>/worker', projectViews.AddWorkerView.as_view()),
    path('api/projects/paginate', projectViews.GetProjectsWithPaginateView.as_view()),
    path('api/projects', projectViews.GetProjectsView.as_view()),
    path('api/project/<int:project_id>/set-complete', projectViews.SetCompleteProjectView.as_view()),
    path('api/project/<int:project_id>', projectViews.GetProjectView.as_view()),
    path('api/project/advance', projectViews.AdvanceView.as_view()),
]
