"""my_drf_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'docs/', include_docs_urls(title='接口文档1')),
    url(r'docs2/', get_schema_view(title='接口文档2', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])),
    url(r'docs3/', get_schema_view(title='接口文档3')),
    url(r'^api/user/', include('user.urls', namespace='user'), name='user'),
]