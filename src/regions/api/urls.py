from rest_framework.routers import DefaultRouter
from .views import RegionViewSet

router = DefaultRouter()
router.register(r'', RegionViewSet, basename='region')

urlpatterns = router.urls
