#!/usr/bin/env python

import sys
sys.path.insert(0, '../')  # meidoo


import os   # 导入配置，其实也可以不需要这些，只是函数他用到了这些
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meidoo.setting.dev'

# 让django进行初始化设置
import django
django.setup()


from meidoo.apps.contents.crons import generate_static_index_html


if __name__ == '__main__':
    generate_static_index_html()