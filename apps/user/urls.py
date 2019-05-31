from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .django_views import TestFBV

from .views import UserViewSet, StudentViewSet

app_name = "user"

# user = UserViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
#
# urlpatterns = [
#     url('', user, name='user')
# ]

user_router = DefaultRouter()
user_router.register(r'^student', StudentViewSet, base_name='student')
user_router.register(r'^normal', UserViewSet, base_name='user')

urlpatterns = [
    url(r'django/testFBV', TestFBV),
    url(r'', include(user_router.urls)),
]
