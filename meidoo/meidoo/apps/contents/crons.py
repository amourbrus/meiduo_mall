import os
from collections import OrderedDict

from django.conf import settings
from django.template import loader
# from rest_framework import settings

from contents.models import ContentCategory
from goods.models import GoodsChannel


def generate_static_index_html():

    # 商品分类数据
    categories = OrderedDict()  # python自带的字典,key, 1,2,3
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')
    """Out[9]: <QuerySet [<GoodsChannel: 手机>, <GoodsChannel: 相机>, <sChannel: 数码>,
    <GoodsChannel: 电脑>, <GoodsChannel: 办公>, <Gonnel: 家用电器>, <GoodsChannel: 家居>, <GoodsChannel: 家具>,
     <Goel: 家装>, <GoodsChannel: 厨具>, <GoodsChannel: 男装>, <GoodsCha女装>, <GoodsChannel: 童装>, <GoodsChannel: 内衣>,
     <GoodsChannel <GoodsChannel: 箱包>, <GoodsChannel: 钟表>, <GoodsChannel: 珠宝odsChannel: 男鞋>, <GoodsChannel: 运动>, '
     ...(remaining elementsncated)...']>
"""
    for channel in channels:
        group_id = channel.group_id
        if group_id not in categories:
            categories[group_id] = {'channels':[], 'sub_cats': []}

        cat1 = channel.category  # 当前频道的类别
        categories[group_id]['channels'].append({
            'id': cat1.id,
            'name': cat1.name,
            'url': channel.url
        })

        for cat2 in cat1.goodscategory_set.all():
            cat2.sub_cats = []
            for cat3 in cat2.goodscategory_set.all():
                cat2.sub_cats.append(cat3)
            categories[group_id]['sub_cats'].append(cat2)


    # 广告数据
    contents = {}
    content_categories = ContentCategory.objects.all()
    print('------', content_categories)
    for cat in content_categories:
        contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

    # 渲染模板
    context = {
        'categories': categories,
        'contents': contents
    }
    # render
    template = loader.get_template('index.html')
    html_text = template.render(context)
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'index.html')
    # 保存数据到文件, html
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_text)




























