from django.urls import path

from main.views import projectViews

urlpatterns = [
    path('api/project', projectViews.ProjectView.as_view()),
    path('api/project/<int:project_id>/time-entry', projectViews.TimeEntryView.as_view()),
]
