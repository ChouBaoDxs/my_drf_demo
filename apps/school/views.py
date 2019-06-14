from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Student, Hobby
from .serializers import StudentSerializer, StudentUpdateSerializer, HobbySerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.filter(is_delete=False)
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['id', 'gender', 'age']
    ordering_fields = ['id', 'age']

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return StudentUpdateSerializer
        return self.serializer_class

    def list(self, request, *args, **kwargs):
        result = super().list(request, *args, **kwargs)
        # print(self.get_serializer_context())
        print(result.data)  # OrderedDict([('count', 0), ('next', None), ('previous', None), ('results', [])])
        return result

    def perform_destroy(self, instance):
        instance.update_is_delete()


class HobbyViewSet(viewsets.ModelViewSet):
    queryset = Hobby.objects.filter(is_delete=False)
    serializer_class = HobbySerializer

    def perform_destroy(self, instance):
        instance.update_is_delete()
