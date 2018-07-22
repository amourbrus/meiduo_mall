from decimal import Decimal
from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from goods.models import SKU
from orders.serializers import OrderSettlementSerializer, SaveOrderSerializer


#  GET /orders/settlement/
class OrderSettlementView(APIView):
    """订单结算　－－－从购物车到订单结算页面"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
    #     获取
        user = request.user
    #     从购物车中获取用户勾选的要结算的商品信息
        redis_conn = get_redis_connection('cart')
        redis_cart = redis_conn.hgetall('cart_%s' % user.id)   # 返回一个列表，包含所有的域和值
        # print('redis_cart', redis_cart)  # list  {b'10': b'1', b'15': b'1'}  list??　sku_id  count
        cart_selected = redis_conn.smembers('cart_selected_%s' % user.id )  # 集合中的所有成员。
        # print('redis_selected', cart_selected)  # {b'10', b'15'}

        # 勾选的商品sku_id  保存到变量cart
        cart = {}
        for sku_id in cart_selected:
            cart[int(sku_id)] = int(redis_cart[sku_id])

        # 查询商品信息
        skus = SKU.objects.filter(id__in=cart.keys())
        # print(skus)   # 商品信息
        for sku in skus:
            sku.count = cart[sku.id]

        # 运费
        freight = Decimal('10.00')

        serializer = OrderSettlementSerializer({'freight':freight, 'skus':skus})
        return Response(serializer.data)

#  POST /orders/
class SaveOrderView(CreateAPIView):
    """保存订单　－－－　数据库"""
    permission_classes = [IsAuthenticated]
    serializer_class = SaveOrderSerializer
