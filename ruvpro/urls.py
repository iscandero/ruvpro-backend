from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .yasg import urlpatterns as doc_urls
from ruvpro import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('main.urls.user_api_urls')),
                  path('', include('main.urls.project_api_urls')),
                  path('', include('main.urls.authorization_api_urls')),
                  path('', include('main.urls.team_api_urls')),
                  path('', include('main.urls.statistics_api_urls')),
                  path('', include('main.urls.history_api_urls')),
                  path('', include('main.urls.codes_api_urls')),
                  path('', include('main.urls.data_links_urls')),
                  path('', include('main.urls.basic_urls')),
                  path('', include('main.urls.report_urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += doc_urls
