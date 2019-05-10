from rest_framework.pagination import (
    PageNumberPagination,
    LimitOffsetPagination,
    CursorPagination
)


# a. 根据页码进行分页
class CtPageNumberPagination(PageNumberPagination):
    page_size = 12  # 默认每页显示的数据条数
    page_size_query_param = 'page_size'  # 获取URL参数中设置的每页显示数据条数
    page_query_param = 'page'  # 获取URL参数中传入的页码key
    max_page_size = 100  # 最大支持的每页显示的数据条数


# b. 位置和个数进行分页
class CtLimitOffsetPagination(LimitOffsetPagination):
    # 默认每页显示的数据条数
    default_limit = 10
    # URL中传入的显示数据条数的参数
    limit_query_param = 'limit'
    # URL中传入的数据位置的参数
    offset_query_param = 'offset'
    # 最大每页显得条数
    max_limit = None


# c. 游标分页
class CtCursorPagination(CursorPagination):
    # URL传入的游标参数
    cursor_query_param = 'cursor'
    # 默认每页显示的数据条数
    page_size = 2
    # URL传入的每页显示条数的参数
    page_size_query_param = 'page_size'
    # 每页显示数据最大条数
    max_page_size = 1000

    # 根据ID从大到小排列
    ordering = "id"
