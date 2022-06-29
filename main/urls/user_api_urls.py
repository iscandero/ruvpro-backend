from django.urls import path

from main.views import usersViews

urlpatterns = [
    path('api/user/settings', usersViews.UserSettingsView.as_view()),
    path('api/user', usersViews.UserView.as_view()),
    path('api/user/settings/<int:role_id>', usersViews.UserViewForIndexInEnd.as_view()),
    path('api/user/change-phone', usersViews.ChangePhone.as_view()),
    path('api/file/upload', usersViews.UploadFile.as_view()),
]
