from rest_framework.routers import DefaultRouter

from areas import views

router = DefaultRouter()

#  (self, prefix, viewset, base_name=None)
router.register(r'areas', views.AreasViewSet, base_name='areas')

urlpatterns = []

urlpatterns += router.urls