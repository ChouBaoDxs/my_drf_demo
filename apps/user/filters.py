import django_filters
from .models import User


class UserFilter(django_filters.rest_framework.FilterSet):
    """
    自定义过滤类
    """
    joined_min = django_filters.DateTimeFilter(name='date_joined', lookup_expr='gte')
    joined_max = django_filters.DateTimeFilter(name='date_joined', lookup_expr='lte')
    username = django_filters.CharFilter(name='username', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['username', 'joined_min', 'joined_max']
