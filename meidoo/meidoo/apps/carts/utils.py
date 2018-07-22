import base64
import pickle

from django_redis import get_redis_connection


def merge_cart_cookie_to_redis(request, user, response):
    """合并请求用户的购物车数据，将未登录保存在cookie里的保存到redis中
    遇到cookie与redis中出现相同的商品时以cookie数据为主，覆盖redis中的数据"""
    cookie_cart = request.COOKIES.get('cart')  # 加密的字典
    if not cookie_cart:
        return response
    # 解密的字典
    cookie_cart = pickle.loads(base64.b64decode(cookie_cart.encode()))
    cart = {}  # 用于保存向redis购物车商品数量hash添加数据的字典

    redis_cart_selected_add = []  # 记录redis勾选状态中应该增加的sku_id
    redis_cart_selected_remove = []  # 记录redis勾选状态中应该删除的sku_id

    # 合并cookie购物车与redis购物车, 保存到cart字典中
    for sku_id, count_selected_dict in cookie_cart.items():
        cart[sku_id] = count_selected_dict['count']

        if count_selected_dict['selected']:
            redis_cart_selected_add.append(sku_id)
        else:
            redis_cart_selected_remove.append(sku_id)

    if cart:
        redis_conn = get_redis_connection('cart')
        pl = redis_conn.pipeline()
        pl.hmset('cart_%s' % user.id, cart)
        if redis_cart_selected_add:
            # SADD key member [member ...]
            pl.sadd('cart_selected_%s' % user.id, *redis_cart_selected_add)
        if redis_cart_selected_remove:
            # SREM key member [member ...]
            pl.srem('cart_selected_%s' % user.id, *redis_cart_selected_remove)
        pl.execute()

    response.delete_cookie('cart')

    return response


