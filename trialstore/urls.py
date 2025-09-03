from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    TrialVendorViewSet, TrialProductViewSet, TrialProductCarouselViewSet,
    TrialProductMilestoneViewSet, TrialStoreAdViewSet, TrialStoreFeedbackViewSet
)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TrialAdViewSet

router = DefaultRouter()
router.register(r"vendors", TrialVendorViewSet, basename="trial-vendors")
router.register(r"products", TrialProductViewSet, basename="trial-products")
router.register(r"carousels", TrialProductCarouselViewSet, basename="trial-carousels")
router.register(r"milestones", TrialProductMilestoneViewSet, basename="trial-milestones")
router.register(r"ads", TrialStoreAdViewSet, basename="trial-ads")
router.register(r"feedbacks", TrialStoreFeedbackViewSet, basename="trial-feedbacks")
router = DefaultRouter()
router.register(r'trial-ads', TrialAdViewSet, basename='trial-ads')

urlpatterns = [
    path("", include(router.urls)),
]

