from django.conf.urls import url
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token

from . import views

router = routers.DefaultRouter()
router.register(r'addresses', views.AddressViewSet, base_name='addresses')

urlpatterns = [
    url(r'^users/$', views.UserView.as_view()),
    # url(r'^authorizations/$', obtain_jwt_token),
    url(r'^authorizations/$', views.UserAuthorizeView.as_view()),
    url(r'^user/$', views.UserDetailView.as_view()),
    url(r'^emails/$', views.EmailView.as_view()),  # 设置邮箱
    url(r'^emails/verification/$', views.VerifyEmailView.as_view()),
    url(r'browse_histories/$', views.UserBrowersingHistoryView.as_view()),
]

urlpatterns += router.urls
# POST /addresses/ 新建  -> create
# PUT /addresses/<pk>/ 修改  -> update
# GET /addresses/  查询  -> list
# DELETE /addresses/<pk>/  删除 -> destroy
# PUT /addresses/<pk>/status/ 设置默认 -> status
# PUT /addresses/<pk>/title/  设置标题 -> title








#
# from django.conf.urls import url
#
# from . import views
#
# urlpatterns = [
#     url(r"image_codes/(?P<image_code_id>[\w-]+)/$", views.ImageCodeView.as_view()),
#     url('^sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view()),
#     url(r'^usernames/(?P<username>\w{5,20})/count/$', views.UsernameCountView.as_view()),
#     url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$', views.MobileCountView.as_view()),
# ]


