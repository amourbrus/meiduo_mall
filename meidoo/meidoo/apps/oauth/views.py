from django.shortcuts import render

# Create your views here.

#  url(r'^qq/authorization/$', views.QQAuthURLView.as_view()),
# from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
# from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from carts.utils import merge_cart_cookie_to_redis
from oauth.exceptions import QQAPIError
from oauth.models import OAuthQQUser
from oauth.serializers import OAuthQQUserSerializer
from oauth.utils import OAuthQQ

# url(r'^qq/authorization/$', views.QQAuthURLView.as_view()),
class QQAuthURLView(APIView):
    """获取QQ登录的url"""
    def get(self, request):
        # 提供qq登录的url
        next = request.query_params.get('next')
        oauth = OAuthQQ(state=next)
        login_url = oauth.get_qq_login_url()

        return Response({'login_url':login_url})


# class QQAuthUserView(APIView):
# url(r'^qq/user/$', views.QQAuthUserView.as_view()),
class QQAuthUserView(CreateAPIView):
    print('****')
    serializer_class = OAuthQQUserSerializer
    """qq登录的用户"""
    def get(self, request):
        """获取qq登录的用户数据"""
        code = request.query_params.get('code')
        if not code:
            return Response({'message': '缺少code'}, status=status.HTTP_400_BAD_REQUEST)
        oauth = OAuthQQ()
        # 获取用户openid
        try:
            access_token = oauth.get_access_token(code)
            print(access_token)
            openid = oauth.get_openid(access_token)
            print("id  ",openid)
        except QQAPIError:
            return Response({'message': 'QQ服务异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        # 判断用户是否存在
        try:
            qq_user = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 用户第一次使用QQ登录
            token = oauth.generate_save_user_token(openid)
            return Response({'access_token': token})
        else:
            # 找到用户, 生成token
            user = qq_user.user
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            response = Response({
                'token': token,
                'user_id': user.id,
                'username': user.username
            })

            # 合并购物车
            response = merge_cart_cookie_to_redis(request,user,response)

            return response

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # 合并购物车
        response = merge_cart_cookie_to_redis(request, self.user, response)
        return response