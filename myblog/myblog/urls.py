"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from unittest.mock import patch

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.permissions import AllowAny

#from rest_framework.schemas import get_schema_view
from drf_yasg.views import get_schema_view


# def patch_the_method(func):
#     def inner(*args, **kwargs):
#         with patch('rest_framework.permissions.IsAuthenticated.has_permission', return_value=True):
#             response = func(*args, **kwargs)
#         return response
#     return inner
#
# schema_view = patch_the_method(get_schema_view(title='API'))

schema_view = get_schema_view(
   openapi.Info(
      title="Drinking Day API",
      default_version='v1',
      description="This API allows us to keep a diary of our daily drinking",
      terms_of_service="https://www.scvconsultants.com",
      contact=openapi.Contact(email="michal@scvconsultants.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('swagger-ui/', TemplateView.as_view(
    #     template_name='swagger-ui.html',
    #     extra_context={'schema_url': 'openapi-schema'}
    # ), name='swagger-ui'),
    # path('openapi', schema_view, name='openapi-schema'),
    path('swaggerjson/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/', include('blog.urls')),
    path('api/v1/auth/', include('djoser.urls')),          # new
    path('api/v1/', include('djoser.urls.authtoken'))      # new
]
