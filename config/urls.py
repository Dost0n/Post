from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from rest_framework import permissions
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView

schema_view = get_schema_view(
    openapi.Info(
        title="Post API",
        default_version="v1",
        description="Post",
        terms_of_services="Post"
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),

    #token
    path('login/', TokenObtainPairView.as_view()),
    # swagger
    path('swagger/', schema_view.with_ui(
        "swagger", cache_timeout=0), name="swagger-swagger-ui"),
    path('redoc/', schema_view.with_ui(
        "redoc", cache_timeout=0), name="schema-redoc"),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)