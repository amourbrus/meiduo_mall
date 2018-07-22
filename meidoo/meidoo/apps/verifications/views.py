import random

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
# from requests import Response
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

# from libs.captcha import captcha
from celery_tasks.sms import tasks
from meidoo.libs.captcha.captcha import captcha
# from libs.yuntongxun.sms import CCP
from users.models import User
from verifications import constants
from verifications import serializers


# GET url('^image_codes/(?P<image_code_id>[\w-]+)/$', views.ImageCodeView.as_view()),
class ImageCodeView(APIView):
    """图片验证码"""
    def get(self,request,image_code_id):
        text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection("verify_codes")
        redis_conn.setex("img_%s"%image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES,text)

        print("image code =====", text)
        return HttpResponse(image, content_type="img/jpg")

# GET url('^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view()),
class SMSCodeView(GenericAPIView):
    """短信"""
    serializer_class = serializers.ImageCodeCheckSerializer

    def get(self,request,mobile):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        # 生成短信验证码
        sms_code = '%06d' % random.randint(0,999999)
        print("短信验证码==>" , sms_code)
        # 保存短信验证码和发送记录
        redis_conn = get_redis_connection('verify_codes')
        p1 = redis_conn.pipeline()  # 队列／管道，减少数据库写入操作
        # string
        p1.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        p1.setex('send_flag_%s'%mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        p1.execute()

        # 发送短信验证码
        sms_code_expires = str(constants.SMS_CODE_REDIS_EXPIRES//60)
        tasks.send_sms_code.delay(mobile, sms_code, sms_code_expires)


        return Response({"message": "OK"})  # 作用是？　还有就是导错了


class UsernameCountView(APIView):
    """用户名数量,大于０就是已经注册"""
    def get(self, request, username):
        count = User.objects.filter(username=username).count()

        data = {
            "username": username,
            "count": count,
        }

        return Response(data)

class MobileCountView(APIView):
    """手机号数量"""
    def get(self,request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        data = {
            'mobile':mobile,
            'count':count,
        }
        return Response(data)


class UserView(CreateAPIView):
    """用户注册"""
    serializer_class = serializers.CreateUserSerializer