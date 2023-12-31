"""
URL configuration for anri project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path

from rocket.apps.objects.views import ChainObjectView


API_PREFIX = "api"
API_V1_PREFIX = f"{API_PREFIX}/v1"


admin_urlpatterns = [
    path("admin/", admin.site.urls),
]

api_v1_urlpatterns = [
    path(
        "objects/",
        ChainObjectView.as_view(),
    ),
    path(
        f"{API_V1_PREFIX}/",
        include(("rocket.apps.objects.urls", "objects"), namespace="api-v1-objects"),
    ),
    path(
        f"{API_V1_PREFIX}/",
        include(("rocket.apps.products.urls", "products"), namespace="api-v1-products"),
    ),
    path(f"{API_V1_PREFIX}/auth/", include("djoser.urls")),
    path(f"{API_V1_PREFIX}/auth/", include("djoser.urls.jwt")),
]

urlpatterns = admin_urlpatterns + api_v1_urlpatterns

if "SWAGGER" in settings.ROCKET_FEATURES:
    from rest_framework import permissions

    from drf_yasg import openapi
    from drf_yasg.views import get_schema_view

    api_v1_schema_view = get_schema_view(
        openapi.Info(
            title="rocket",
            default_version="v1",
            description="Rocket API v1 description",
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
        patterns=api_v1_urlpatterns,
    )

    swagger_urlpatterns = [
        re_path(
            f"{API_V1_PREFIX}/" + r"swagger(?P<format>\.json|\.yaml)$",
            api_v1_schema_view.without_ui(cache_timeout=0),
            name="v1-schema-json",
        ),
        path(
            f"{API_V1_PREFIX}/swagger/",
            api_v1_schema_view.with_ui("swagger", cache_timeout=0),
            name="v1-schema-swagger-ui",
        ),
        path(
            f"{API_V1_PREFIX}/",
            api_v1_schema_view.with_ui("redoc", cache_timeout=0),
            name="v1-schema-redoc",
        ),
    ]

urlpatterns += swagger_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
