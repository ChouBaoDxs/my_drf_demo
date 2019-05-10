from rest_framework import serializers

from .models import User


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
        return "xxx"

    def create(self, validated_data):
        return super().create(validated_data)

    # 自定义字段验证
    # pwd = serializers.CharField(error_messages={'required': '密码不能为空'}, validators=[PasswordValidator('666')])


class ModelUserSerializer(serializers.ModelSerializer):
    user = serializers.CharField(max_length=32)
    ut = serializers.HyperlinkedIdentityField(view_name='detail')   # c. 生成URL

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
