from django.urls import path

from main.views.links_views import LinkListAPIView

urlpatterns = [
    path('api/links', LinkListAPIView.as_view()),
]
