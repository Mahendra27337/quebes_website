from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MilestoneSetViewSet, MilestoneViewSet, UserMilestoneViewSet

router = DefaultRouter()
router.register(r"milestone-sets", MilestoneSetViewSet, basename="milestone-set")
router.register(r"milestones", MilestoneViewSet, basename="milestone")
router.register(r"user-milestones", UserMilestoneViewSet, basename="user-milestone")

urlpatterns = [
    path("", include(router.urls)),
]
