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
from rest_framework.schemas import get_schema_view as drf_get_schema_view
# from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
import xadmin
from rest_framework_extensions.routers import ExtendedSimpleRouter

from school.views import StudentViewSet, HobbyViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# drf自带的Router只支持1级(https://www.django-rest-framework.org/api-guide/routers/)
# 如果要多级路由，需要借助drf-extensions
router = ExtendedSimpleRouter(trailing_slash=False)  # 不强制在url结尾加上/
nested_item = router.register(r'api/v1/student', StudentViewSet, base_name='robot')

nested_item.register(r'hobby',
                     HobbyViewSet,
                     basename='student-hobby',
                     parents_query_lookups=['student_hobby'])

urlpatterns = [
    # path('admin/', admin.site.urls),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # url(r'docs/', include_docs_urls(title='接口文档1')),
    # url(r'docs2/', get_schema_view(title='接口文档2', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])),
    url(r'docs3/', drf_get_schema_view(title=u'接口文档3')),
    url(r'^api/user/', include('user.urls', namespace='api_user'), name='user'),

    # xadmin
    url(r'^xadmin/', xadmin.site.urls),

    path('', include(router.urls)),
]
