from django.urls import path

from main.views.team_views import base_team_views

urlpatterns = [
    path('api/team', base_team_views.GetUsersByTeam.as_view()),

]
