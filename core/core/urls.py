"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework.schemas import get_schema_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.schemas.openapi import SchemaGenerator

from .views import RootAPI


class TOSSchemaGenerator(SchemaGenerator):
    def get_schema(self, *args, **kwargs):
        schema = super().get_schema(*args, **kwargs)
        schema["info"]["termsOfService"] = "https://example.com/tos.html"
        return schema


urlpatterns = [
    path('admin/', admin.site.urls),

    # OpenAPI schema
    path('openapi/', get_schema_view(
        title='STAR BANK',
        description='API schema for all endpoints',
        version='1.0',
        permission_classes=[AllowAny],
        generator_class=TOSSchemaGenerator,
    ), name='openapi-schema'),

    # SwaggerUI for schema
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger/swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'},
    ), name='swagger-ui'),

    path('__debug__/', include('debug_toolbar.urls')),
    path('api/v1/auth/', include('rest_framework.urls')),

    path('api/v1/', RootAPI.as_view(), name='root'),

    path('api/v1/', include('bank.urls')),
    path('api/v1/', include('user.urls')),
]
