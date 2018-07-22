from rest_framework import serializers  # 手动？

# from areas.models import Area
from .models import Area


class AreaSerializer(serializers.ModelSerializer):
    """行政区信息序列化器"""
    class Meta:
        model = Area
        fields = ('id','name')

class SubAreaSerializer(serializers.ModelSerializer):
    """子行政区划信息序列化器"""
    subs = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = ('id', 'name', 'subs')

