from django.shortcuts import render

# Create your views here.

# class AreasViewSet(ReadOnlyModel)
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from areas.models import Area
from areas.serializers import AreaSerializer, SubAreaSerializer


class AreasViewSet(CacheResponseMixin,ReadOnlyModelViewSet):
    pagination_class = None    # 不分页

    def get_queryset(self):
        if self.action == 'list':
            return Area.objects.filter(parent=None)

        else:
            return Area.objects.all()

    def get_serializer_class(self):

        if self.action == 'list':
            return AreaSerializer
        else:
            return SubAreaSerializer