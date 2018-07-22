from collections import OrderedDict

from .models import GoodsChannel


def get_categories():
    """
    获取商城商品分类菜单
    :return 菜单字典
    """
    # 商品频道及分类菜单
    # 使用有序字典保存类别的顺序
    # categories = {
    #     1: { # 组1
    #         'channels': [{'id':, 'name':, 'url':},{}, {}...],
    #         'sub_cats': [{'id':, 'name':, 'sub_cats':[{},{}]}, {}, {}, ..]
    #     },
    #     2: { # 组2
    #
    #     }
    # }
    categories = OrderedDict()
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')
    """
In [5]: GoodsChannel.objects.order_by('group_id','sequence')
Out[5]: <QuerySet [<GoodsChannel: 手机>, <GoodsChannel: 相机>, <GoodsChannel: 数码>, <hannel: 电脑>, <GoodsChannel: 办公>, <GoodsChannel: 家用电器>, <GoodsChannel: 家居>, <el: 家具>, <GoodsChannel: 家装>, <GoodsChannel: 厨具>, <GoodsChannel: 男装>, <GoodsCha>, <GoodsChannel: 童装>, <GoodsChannel: 内衣>, <GoodsChannel: 女鞋>, <GoodsChannel: 箱odsChannel: 钟表>, <GoodsChannel: 珠宝>, <GoodsChannel: 男鞋>, <GoodsChannel: 运动>, 'ining elements truncated)...']>
In [6]: channels = GoodsChannel.objects.order_by('group_id','sequence')
In [11]: channels[0]
Out[11]: <GoodsChannel: 手机>
In [9]: cat1 = channels[0].category
In [10]: cat1
Out[10]: <GoodsCategory: 手机>
In [14]: cat2 = cat1.goodscategory_set.all()
In [15]: cat2
Out[15]: <QuerySet [<GoodsCategory: 手机通讯>, <GoodsCategory: 手机配件>]>
In [17]: cat2[0].goodscategory_set.all()
Out[17]: <QuerySet [<GoodsCategory: 手机>, <GoodsCategory: 游戏手机>, <GoodsCategory: 老人机>, egory: 对讲机>]>
In [18]: cat3 = cat2[0].goodscategory_set.all()
In [19]: cat3[0]
Out[19]: <GoodsCategory: 手机>


    """
    for channel in channels:
        group_id = channel.group_id  # 当前组
#
        if group_id not in categories:
            categories[group_id] = {'channels': [], 'sub_cats': []}

        cat1 = channel.category  # 当前频道的类别

        # 追加当前频道
        categories[group_id]['channels'].append({
            'id': cat1.id,
            'name': cat1.name,
            'url': channel.url
        })
        # 构建当前类别的子类别
        # print("======",cat1.goodscategory_set.all())
        for cat2 in cat1.goodscategory_set.all():
            cat2.sub_cats = []
            for cat3 in cat2.goodscategory_set.all():
                cat2.sub_cats.append(cat3)
            categories[group_id]['sub_cats'].append(cat2)  # 可以移到前面去
    return categories




