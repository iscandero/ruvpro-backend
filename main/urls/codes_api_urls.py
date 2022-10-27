from django.urls import path

from main.views.codes_views import CodeRoleListAPIView

urlpatterns = [
    path('api/codes/roles', CodeRoleListAPIView.as_view()),

]
