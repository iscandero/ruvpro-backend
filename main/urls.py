from django.urls import path

from . import usersViews

# Создание путей
urlpatterns = [
    path('user/signup', usersViews.UserRegistry.as_view()),
    path('user/login', usersViews.UserLogin.as_view()),
    path('api/user/settings', usersViews.UserView.as_view()),

]
