from django.utils import six
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework import viewsets, status

class DRFExtend(object):
    class CodeMsgResponse(Response):

        def __init__(self, data=None, status=None,
                     template_name=None, headers=None,
                     exception=False, content_type=None,
                     code=0, msg='success'):  # 自定义添加的两个字段
            super(Response, self).__init__(None, status=status)

            if isinstance(data, Serializer):
                msg = (
                    'You passed a Serializer instance as data, but '
                    'probably meant to pass serialized `.data` or '
                    '`.error`. representation.'
                )
                raise AssertionError(msg)

            self.data = {"code": code, "msg": msg, "data": data}  # 设置返回的数据格式，带上code和msg
            self.template_name = template_name
            self.exception = exception
            self.content_type = content_type

            if headers:
                for name, value in six.iteritems(headers):
                    self[name] = value

    class CodeMsgResponseModelViewSet(viewsets.ModelViewSet):
        def dispatch(self, request, *args, **kwargs):
            data = super().dispatch(request, *args, **kwargs)
            print('CodeMsgResponseModelViewSet：',data)
            return data

        def create(self, request, *args, **kwargs):
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return DRFExtend.CodeMsgResponse(data=serializer.data, msg="success", code=0, status=status.HTTP_201_CREATED, headers=headers)

        def list(self, request, *args, **kwargs):
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                # return self.get_paginated_response(serializer.data)
                return DRFExtend.CodeMsgResponse(data=self.get_paginated_response(serializer.data).data, code=0, msg="success")

            serializer = self.get_serializer(queryset, many=True)
            return DRFExtend.CodeMsgResponse(data=serializer.data, code=0, msg="success")

        def retrieve(self, request, *args, **kwargs):
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return DRFExtend.CodeMsgResponse(data=serializer.data, code=0, msg="success")

        def update(self, request, *args, **kwargs):
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
                # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}

            return DRFExtend.CodeMsgResponse(data=serializer.data, msg="success", code=0)

        def destroy(self, request, *args, **kwargs):
            instance = self.get_object()
            self.perform_destroy(instance)
            return DRFExtend.CodeMsgResponse(data=[], code=0, msg="delete resource success", status=status.HTTP_204_NO_CONTENT)
