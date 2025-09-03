from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReligiousStoreViewSet

router = DefaultRouter()
router.register(r'religious-store', ReligiousStoreViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
