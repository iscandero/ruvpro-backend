from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from ruvpro import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('main.urls.user_api_urls')),
                  path('', include('main.urls.project_api_urls')),
                  path('', include('main.urls.authorization_api_urls')),
                  path('', include('main.urls.team_api_urls')),
                  path('', include('main.urls.statistics_api_urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
