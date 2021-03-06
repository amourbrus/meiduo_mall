import json
from urllib.parse import urlencode, parse_qs
from urllib.request import urlopen

from django.conf import settings

from meidoo.utils.exceptions import logger
from oauth import constants
from oauth.exceptions import QQAPIError
from itsdangerous import TimedJSONWebSignatureSerializer as ser, BadData


class OAuthQQ(object):
    """QQ认证辅助工具类"""
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, state=None):
        self.client_id = client_id or settings.QQ_CLIENT_ID
        self.client_secret = client_secret or settings.QQ_CLIENT_SECRET
        self.redirect_uri = redirect_uri or settings.QQ_REDIRECT_URI
        self.state = state or settings.QQ_STATE  # 用于保存登录成功后的跳转页面路径


    def get_qq_login_url(self):
        """
        获取qq登录的地址
        返回url
        """
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': self.state,
        }

        # https://graph.qq.com/oauth2.0/authorize  来自qq互联文档
        # 注意添加问号，　urlencode 字典　to str
        url = 'https://graph.qq.com/oauth2.0/authorize?' + urlencode(params)

        return url

    def get_access_token(self, code):
        """
        获取access_token
        :param code: qq提供的code
        :return: access_token
        """
        params = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri
        }

        url = 'https://graph.qq.com/oauth2.0/token?' + urlencode(params)

        resp = urlopen(url)
        resp_data = resp.read().decode()
        data = parse_qs(resp_data)
        access_token = data.get('access_token', None)

        if not access_token:
            logger.error('code=%s msg=%s' % (data.get('code'), data.get('msg')))
            raise QQAPIError  #  新建一个exceptions

        print(access_token)
        return access_token[0]


    def get_openid(self, access_token):
        """
                获取用户的openid
                :param access_token: qq提供的access_token
                :return: open_id
                """
        url = 'https://graph.qq.com/oauth2.0/me?' + 'access_token=' + access_token

        response = urlopen(url)
        response_data = response.read().decode()
        print(response_data)
        try:
            # 返回的数据 callback( {"client_id":"YOUR_APPID","openid":"YOUR_OPENID"} )\n;
            data = json.loads(response_data[10:-4])
        except Exception:
            data = parse_qs(response_data)
            logger.error('code=%s msg=%s' % (data.get('code'), data.get('msg')))
            raise QQAPIError
        openid = data.get('openid', None)
        return openid

    @staticmethod
    def generate_save_user_token(openid):
        """
        生成保存用户数据的token
        :param openid: 用户的openid
        :return: token
        """
        serializer = ser(settings.SECRET_KEY, expires_in=constants.SAVE_QQ_USER_TOKEN_EXPIRES)
        data = {'openid': openid}
        token = serializer.dumps(data)
        return token.decode()

    @staticmethod
    def check_save_user_token(token):
        """验证保存用户数据的token"""
        serializer = ser(settings.SECRET_KEY, expires_in=constants.SAVE_QQ_USER_TOKEN_EXPIRES)
        try:
            data = serializer.loads(token)
        except BadData:
            return None
        else:
            return data.get('openid')