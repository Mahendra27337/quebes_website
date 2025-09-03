from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DigitalProductViewSet, DigitalPurchaseViewSet

router = DefaultRouter()
router.register(r"products", DigitalProductViewSet)
router.register(r"purchases", DigitalPurchaseViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
