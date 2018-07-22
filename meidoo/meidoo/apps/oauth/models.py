from django.db import models

# Create your models here.
# from utils.models import BaseModel
from meidoo.utils.models import BaseModel


class OAuthQQUser(BaseModel):
    """QQ登录用户数据"""

    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='用户')
    # users.User  ???
    openid = models.CharField(max_length=64, verbose_name='openid', db_index=True)

    class Meta:
        db_table = 'tb_oauth_qq'
        verbose_name = 'qq登录用户数据'
        verbose_name_plural = verbose_name  # 显示的复数名称

