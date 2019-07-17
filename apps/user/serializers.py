from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import *


class PasswordValidator(object):
    def __init__(self, base):
        self.base = base

    def __call__(self, value):
        if value != self.base:
            message = 'This field must be %s.' % self.base
            raise serializers.ValidationError(message)

    def set_context(self, serializer_field):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # 执行验证之前调用,serializer_fields是当前字段对象
        pass


# a. 自定义字段，继承serializers.Serializer
class UserSerializer1(serializers.Serializer):
    ut_title = serializers.CharField(source='ut.title')
    user = serializers.CharField(min_length=6)
    pwd = serializers.CharField(error_messages={'required': '密码不能为空'}, validators=[PasswordValidator('666')])


# b. 基于Model自动生成字段serializers.ModelSerializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'xxx']

    # current_user默认是当前登录的user
    # current_user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # 返回的字段逻辑比较复杂,可以用serializer.SerializerMethodField()来完成
    xxx = serializers.SerializerMethodField()

    # 把逻辑写在get_的前缀加xxx(字段名),然后返回
    def get_xxx(self, obj):
        # 完成你的业务逻辑
        return 'xxx'

    def create(self, validated_data):
        return super().create(validated_data)

    # 自定义字段验证
    # pwd = serializers.CharField(error_messages={'required': '密码不能为空'}, validators=[PasswordValidator('666')])


class ModelUserSerializer(serializers.ModelSerializer):
    user = serializers.CharField(max_length=32)
    ut = serializers.HyperlinkedIdentityField(view_name='detail')  # c. 生成URL

    class Meta:
        model = User
        fields = "__all__"
        # fields = ['user', 'pwd', 'ut']
        depth = 2
        extra_kwargs = {'username': {'min_length': 6}, 'password': {'validators': [PasswordValidator(666), ]}}
        # read_only_fields = ['user']


# d.自动生成url
class ModelUserSerializer1(serializers.HyperlinkedModelSerializer):
    ll = serializers.HyperlinkedIdentityField(view_name='xxxx')
    tt = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = "__all__"
        list_serializer_class = serializers.ListSerializer

        extra_kwargs = {
            'user': {'min_length': 6},
            'pwd': {'validators': [PasswordValidator(666), ]},
            'url': {'view_name': 'xxxx'},
            'ut': {'view_name': 'xxxx'},
        }


class StudentSerializer(serializers.ModelSerializer):   # ModelSerializer继承自Serializer，实现了简单的create和update方法
# class StudentSerializer(serializers.HyperlinkedModelSerializer):  # HyperlinkedModelSerializer继承自ModelSerializer，可以显示超链接
    # grade = GradeSerializer(required=False) # 包含另一个模型，数据类型为一个，required=False表示接受空
    # teachers = TeacherSerializer(many=True)  # 附带另一个模型，数据类型为列表

    # 可以明确指定字段
    # url = serializers.CharField(source='get_absolute_url', read_only=True)
    # groups = serializers.PrimaryKeyRelatedField(many=True)

    # 设置默认值为当前用户
    # user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Student
        fields = ['id', 'name', 'age', 'gender', 'learn_time', 'learn_time_minute']
        read_only_fields = ['learn_time']  # editable=False的字段和AutoField默认情况下已经为只读，不需要添加到read_only_fields选项中
        exclude = []  # 可以排除要显示的字段，一般不用，直接在fields里写要显示的字段即可，fields和exclude必须提供其中一个
        # extra_kwargs = {'password': {'write_only': True}} # 这个extra_kwargs可以传任意参数给字段，如果出现在这里的字段已经被声明过了，这里会被忽略
        # extra_kwargs = {'url': {'view_name': 'user:student:student-detail'}}

        # validators = UniqueTogetherValidator(  # 数据唯一性校验器
        #     queryset=Student.objects.all(),
        #     fields=['name', 'class']
        # )
        ref_name = 'user.serializers.StudentSerializer'

    # 自定义复杂逻辑字段
    learn_time_minute = serializers.SerializerMethodField()

    def get_learn_time_minute(self, instance):
        return instance.learn_time // 60

    def create(self, validated_data):
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
