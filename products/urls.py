from .views import ProductView, DemoView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'products', ProductView, basename='product')
router.register(r'demo', DemoView, basename='demo')

urlpatterns = router.urls
