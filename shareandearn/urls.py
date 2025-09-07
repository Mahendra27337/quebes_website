from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ShareAndEarnOfferViewSet, ShareAndEarnMilestoneViewSet, ReferralViewSet

router = DefaultRouter()
router.register(r"offers", ShareAndEarnOfferViewSet)
router.register(r"milestones", ShareAndEarnMilestoneViewSet)
router.register(r"referrals", ReferralViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
