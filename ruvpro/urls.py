from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls.user_api_urls')),
    path('', include('main.urls.project_api_urls')),
    path('', include('main.urls.authorization_api_urls')),
]
