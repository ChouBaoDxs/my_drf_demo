from rest_framework.permissions import BasePermission


class CustomPermissionCheck(BasePermission):
    message = "权限验证失败"

    def has_permission(self, request, view):
        """
        判断是否有权限访问当前请求
        Return `True` if permission is granted, `False` otherwise.
        :param request:
        :param view:
        :return: True有权限；False无权限
        """
        if request.user == "管理员":
            return True

    # GenericAPIView中get_object时调用
    def has_object_permission(self, request, view, obj):
        """
        视图继承GenericAPIView，并在其中使用get_object时获取对象时，触发单独对象权限验证
        Return `True` if permission is granted, `False` otherwise.
        :param request:
        :param view:
        :param obj:
        :return: True有权限；False无权限
        """
        if request.user == "管理员":
            return True
