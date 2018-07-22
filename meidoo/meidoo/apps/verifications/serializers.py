from django_redis import get_redis_connection
from rest_framework import serializers
# from rest_framework.serializers import Serializer
# todo how to import whats different
from users.models import User


class ImageCodeCheckSerializer(serializers.Serializer):
    """图片验证码校验序列化器"""
    # 图片验证码编号
    image_code_id = serializers.UUIDField()
    # 用户输入的图片验证码
    text = serializers.CharField(max_length=4,min_length=4)

    # many fields validate use 'validate'
    def validate(self, attrs):
        """validate"""

        image_code_id = attrs['image_code_id']
        text = attrs['text']

        # 查询真实图片验证码, 1, query redis  2, redis_obj.get(image_code_key)
        redis_coon = get_redis_connection('verify_codes')
        real_image_code_text = redis_coon.get('img_%s'%image_code_id)
        # if not exist, expire
        if not real_image_code_text:
            raise serializers.ValidationError("图片验证码无效")

        # 删除图片验证码
        redis_coon.delete('img_%s' % image_code_id,)

        # 比较图片验证码
        real_image_code_text = real_image_code_text.decode()
        if real_image_code_text.lower() != text.lower():
            raise serializers.ValidationError("图片验证码错误")

        # 判断是否在60s内
        mobile = self.context['view'].kwargs['mobile']
        send_flag = redis_coon.get('send_flag_%s' % mobile)
        if send_flag:
            raise serializers.ValidationError("请求次数过于频繁")

        return attrs


class CreateUserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(label="确认密码",write_only=True)
    sms_code = serializers.CharField(label="短信验证吗",write_only=True)
    allow = serializers.CharField(label="同意协议",write_only=True)

    class Meta:
        model = User
        fields = ("id","username","password","password2","sms_code","mobile","allow")
        extra_kwargs = {
            "username": {
                "min_length": 5,
                "max_length": 20,
                "error_message": {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            "password":{
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }

        }

        def validate_mobile(self, value):
            pass