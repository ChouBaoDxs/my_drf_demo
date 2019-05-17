import coreapi
import coreschema
from django.shortcuts import render
from drf_yasg import openapi
from rest_framework import mixins
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.schemas import ManualSchema
from rest_framework.decorators import action
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .models import User
from .serializers import UserSerializer
from .paginationa import CtPageNumberPagination
from base.CustomBaseViewSet import CustomBaseViewSet

import coreapi
from rest_framework.schemas import AutoSchema


# 自定义额外的参数
class MallViewSchema(AutoSchema):   # drf自己的schema定制
    def get_manual_fields(self, path, method):
        extra_fields = []
        if method == 'GET':
            extra_fields = [
                coreapi.Field(
                    "custom_field",
                    required=True,
                    location="query",
                ),
            ]
        manual_fields = super().get_manual_fields(path, method)
        return manual_fields + extra_fields


# class UserViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
# class UserViewSet(CustomBaseViewSet):
class UserViewSet(viewsets.ModelViewSet):
    schema = MallViewSchema()
    """
    retrieve:
       Return a user instance.
    list:
       Return all users, ordered by most recently joined.
    create:
       Create a new user.
    delete:
       Remove an existing user.
    partial_update:
       Update one or more fields on an existing user.
    update:
       Update a user.
    """
    # throttle_classes = (UserRateThrottle, AnonRateThrottle)  # 接口访问频率限制
    # permission_classes = (IsAuthenticated,)  # 权限认证类
    # authentication_classes = [JSONWebTokenAuthentication, SessionAuthentication]  # 配置认证类
    # queryset = User.objects.all() # 重写get_queryset()方法代替
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['id', 'username']
    # filter_class = UserFilter # 可以自定义过滤类
    lookup_field = 'id'
    ordering_fields = ['id', 'email']  # 自定义email
    ordering = ['id', ]  # 默认排序
    search_fields = ['username', 'email']
    pagination_class = CtPageNumberPagination  # 自定义分页器

    # 灵活定制queryset
    def get_queryset(self):
        user_id = self.request.query_params.get('userId') or self.request.data.get('userId')
        if user_id is not None:
            return User.objects.filter(id=user_id)
        return User.objects.all()

    # 灵活定制serializer_class
    def get_serializer_class(self):
        if self.action == 'create':
            return UserSerializer
        elif self.action == 'list':
            return UserSerializer
        return UserSerializer

    test_param = openapi.Parameter('test', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_BOOLEAN)
    user_response = openapi.Response('response description', UserSerializer)

    @swagger_auto_schema(method='get', manual_parameters=[test_param], responses={200: user_response}) # drf_yasg的schema配置
    @action(detail=True, methods=['GET'], url_path='custom_path')
    def custom_path(self, request, *args, **kwargs):
        print(args, kwargs)
        return Response({'msg': 'ok'})
