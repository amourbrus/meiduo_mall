from django.shortcuts import render

# Create your views here.
from drf_haystack.viewsets import HaystackViewSet
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView

from goods.models import SKU
from goods.serialzers import SKUSerializer, SKUIndexSerializer


class SKUListView(ListAPIView):
    """
    sku列表数据
    """
    # 使用的序列化器
    serializer_class = SKUSerializer
    # 过滤后端
    filter_backends = (OrderingFilter,)
    # 过滤的字段
    ordering_fields = ('create_time', 'price', 'sales')

    def get_queryset(self):
        '''
        重写方法获取指定的数据
        :return:
        '''
        # 商品的类别id
        category_id = self.kwargs['category_id']
        return SKU.objects.filter(category_id=category_id, is_launched=True )


class SKUSearchViewSet(HaystackViewSet):
    """
    SKU搜索
    """
    index_models = [SKU]  # 指明哪些

    serializer_class = SKUIndexSerializer