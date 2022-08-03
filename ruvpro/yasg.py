from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="RuvPro API",
        default_version='v1',
    ),
    public=False,
    permission_classes=[permissions.IsAdminUser, ],

)

urlpatterns = [
    path("docs", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
]
