from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from ruvpro import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls.user_api_urls')),
    path('', include('main.urls.project_api_urls')),
    path('', include('main.urls.authorization_api_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
