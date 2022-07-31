from django.urls import path, include

from main.views.team_views import getters_team_views, post_team_view, delete_team_views

urlpatterns = [
    path('api/', include([
        path('team', getters_team_views.GetUsersByTeam.as_view()),
        path('users/<int:user_id>/projects', getters_team_views.GetProjectsByTeamUser.as_view()),
        path('team/worker', post_team_view.AddUserToTeam.as_view()),
        path('team/worker/<int:user_id>', delete_team_views.DeleteUserByTeam.as_view()),
    ]))
]
