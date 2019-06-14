from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import *


class HobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Hobby
        fields = ['id', 'name']


class StudentSerializer(serializers.ModelSerializer):  # ModelSerializer继承自Serializer，实现了简单的create和update方法

    class Meta:
        model = Student
        fields = ['id', 'name', 'age', 'gender', 'created_at', 'updated_at', 'is_delete']
        read_only_fields = ['']

    def create(self, validated_data):
        # user = serializers.CurrentUserDefault()
        # print(user.user) # 不能这样

        request = self.context['request']
        print(request.user)
        # return Student.objects.create(**validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # instance.email = validated_data.get('email', instance.email)
        # email = self.validated_data['email']
        # instance.save()
        # return instance
        return super().update(instance, validated_data)

    def validate_name(self, value):  # 验证单个字段，validate_+字段名
        if not value:
            raise serializers.ValidationError("The name cannot be empty.")
        return value

    def validate(self, attrs):  # 如果验证涉及这个对象的多个字段，可以重写这个validate方法
        # if attrs['created_at'] > attrs['updated_at']:
        #     raise serializers.ValidationError("finish must occur after start")
        return attrs

    # 如果要写成验证器
    """
    def multiple_of_ten(value):
        if value % 10 != 0:
            raise serializers.ValidationError('Not a multiple of ten')

    class GameRecord(serializers.Serializer):
        score = IntegerField(validators=[multiple_of_ten])
    """


class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'age', 'gender', 'created_at', 'updated_at', 'is_delete']
        read_only_fields = ['age']
