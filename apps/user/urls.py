from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .django_views import TestFBV

from .views import UserViewSet

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
user_router.register(r'', UserViewSet, base_name='user')

urlpatterns = [
    url(r'django/testFBV', TestFBV),
    url(r'', include(user_router.urls)),
]
