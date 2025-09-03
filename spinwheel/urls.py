from django.urls import path
from .views import (
    SpinSegmentListCreateView,
    SpinSettingsView,
    PublicSegmentsView,
    SpinWheelView,
    SpinHistoryView,
)

urlpatterns = [
    # Admin
    path("segments/", SpinSegmentListCreateView.as_view(), name="spin-segments-admin"),
    path("settings/", SpinSettingsView.as_view(), name="spin-settings"),

    # Public/User
    path("segments/public/", PublicSegmentsView.as_view(), name="spin-segments-public"),
    path("spin/", SpinWheelView.as_view(), name="spin-wheel"),
    path("history/", SpinHistoryView.as_view(), name="spin-history"),
]
