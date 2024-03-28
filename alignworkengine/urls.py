from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from accounts import views as accounts_views

router = DefaultRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="AlignWork API",
        default_version="v1",
        description="This is the documentation for AlignWork API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],
)

default_urlpatterns = [
    path("admin/", admin.site.urls),
]

custom_urlpatterns = [
    path("api/", include("assistant.urls")),
    path("api/auth/", include("accounts.urls")),
    path("api/documents/", include("documents.urls")),
    path("api/meetings/", include("meetings.urls")),
    path("api/updates/", include("updates.urls")),
    path("api/notifications/", include("notifications.urls")),
    path("api/analytics/", include("analytics.urls")),
    path("api/projects/", include("projects.urls")),
]

spectacular_urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
] + router.urls

swagger_urlpatterns = [
    path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

gauth_urlpatterns = [
    path("google-login/", accounts_views.GoogleLogin.as_view(), name="google-login"),
    path("oauth2callback/", accounts_views.oauth2callback, name="oauth2callback"),
    path(
        "google/notifications/",
        accounts_views.google_notification,
        name="google-notification",
    ),
]

urlpatterns = (
    default_urlpatterns
    + custom_urlpatterns
    + spectacular_urlpatterns
    + swagger_urlpatterns
    + gauth_urlpatterns
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += staticfiles_urlpatterns()
