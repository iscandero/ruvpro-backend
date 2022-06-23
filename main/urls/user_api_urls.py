from django.urls import path

from main.views import usersViews

urlpatterns = [
    path('user/signup', usersViews.UserRegistry.as_view()),
    path('user/login', usersViews.UserLogin.as_view()),
    path('api/user/settings', usersViews.UserSettingsView.as_view()),
    path('api/user', usersViews.UserView.as_view()),
    path('api/user/settings/<int:role_id>', usersViews.UserViewForIndexInEnd.as_view()),
    path('api/user/logout', usersViews.LogOutView.as_view()),
    path('api/user/change-phone', usersViews.ChangePhone.as_view()),
]
