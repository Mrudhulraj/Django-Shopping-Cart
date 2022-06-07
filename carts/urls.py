from .views import CartView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'cartitems', CartView, basename='cartitems')

urlpatterns = router.urls
