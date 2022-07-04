from django.urls import path

from main.views.team_views import getters_team_views, post_team_view, delete_team_views

urlpatterns = [
    path('api/team', getters_team_views.GetUsersByTeam.as_view()),
    path('api/users/<int:user_id>/projects', getters_team_views.GetProjectsByTeamUser.as_view()),
    path('api/team/worker', post_team_view.AddUserToTeam.as_view()),
    path('api/team/worker/<int:user_id>', delete_team_views.DeleteUserByTeam.as_view()),

]
