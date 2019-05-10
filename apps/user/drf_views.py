from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.versioning import (
    QueryParameterVersioning,
    URLPathVersioning,
    AcceptHeaderVersioning,
    HostNameVersioning,
    NamespaceVersioning
)
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser, FileUploadParser

from base.CustomAuthentication import CustomTokenAuthentication, CustomAuthAuthentication
from base.CustomPermissionCheck import CustomPermissionCheck
from base.CustomThrottle import (
    CustomThrottle,
    CustomSimpleRateThrottle,
    CustomScopedRateThrottle,
    LuffyUserRateThrottle,
    LuffyAnonRateThrottle
)
from .serializers import ModelUserSerializer
from .models import User


class TestView(APIView):
    """
    APIView的源码：
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    parser_classes = api_settings.DEFAULT_PARSER_CLASSES
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
    throttle_classes = api_settings.DEFAULT_THROTTLE_CLASSES
    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES
    content_negotiation_class = api_settings.DEFAULT_CONTENT_NEGOTIATION_CLASS
    metadata_class = api_settings.DEFAULT_METADATA_CLASS
    versioning_class = api_settings.DEFAULT_VERSIONING_CLASS
    """

    authentication_classes = [CustomTokenAuthentication, CustomAuthAuthentication]
    permission_classes = [CustomPermissionCheck]
    throttle_classes = [CustomThrottle, CustomSimpleRateThrottle, CustomScopedRateThrottle, LuffyUserRateThrottle, LuffyAnonRateThrottle]
    throttle_scope = "test_scope"  # 和CustomScopedRateThrottle配合使用的

    # 解析器：
    # 仅处理请求头content-type为application/json的请求体
    # parser_classes = [JSONParser]
    # 仅处理请求头content-type为application/x-www-form-urlencoded 的请求体
    # parser_classes = [FormParser]
    # 仅处理请求头content - type为multipart / form - data的请求体
    # parser_classes = [MultiPartParser]
    # 仅上传文件
    # parser_classes = [FileUploadParser]
    # 当同时使用多个parser时，rest framework会根据请求头content-type自动进行比对，并使用对应parser

    # 各种版本解析
    # versioning_class = QueryParameterVersioning
    # versioning_class = URLPathVersioning
    # versioning_class = AcceptHeaderVersioning
    # versioning_class = HostNameVersioning
    # versioning_class = NamespaceVersioning

    def dispatch(self, request, *args, **kwargs):
        """
        请求到来之后，都要执行dispatch方法，dispatch方法根据请求方式不同触发 get/post/put等方法

        注意：APIView中的dispatch方法有好多好多的功能
        """
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        # 获取版本
        print(request.version)
        # 获取版本管理的类
        print(request.versioning_scheme)
        # 反向生成URL
        reverse_url = request.versioning_scheme.reverse('test', request=request)
        print(reverse_url)
        return Response('GET请求，响应内容')

    def get2(self, request, *args, **kwargs):
        # 序列化，将数据库查询字段序列化为字典
        data_list = User.objects.all()
        ser = ModelUserSerializer(instance=data_list, many=True)
        # 或
        # obj = models.UserInfo.objects.all().first()
        # ser = UserSerializer(instance=obj, many=False)
        return Response(ser.data)

    def post(self, request, *args, **kwargs):
        return Response('POST请求，响应内容')

    def post2(self, request, *args, **kwargs):
        # 验证，对请求发来的数据进行验证
        print(request.data)
        ser = ModelUserSerializer(data=request.data)
        if ser.is_valid():
            print(ser.validated_data)
        else:
            print(ser.errors)

        return Response('POST请求，响应内容')

    def put(self, request, *args, **kwargs):
        return Response('PUT请求，响应内容')

    def throttled(self, request, wait):
        """
        访问次数被限制时，定制错误信息
        """

        class Throttled(exceptions.Throttled):
            default_detail = '请求被限制.'
            extra_detail_singular = '请 {wait} 秒之后再重试.'
            extra_detail_plural = '请 {wait} 秒之后再重试.'

        raise Throttled(wait)
