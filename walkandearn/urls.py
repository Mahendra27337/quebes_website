from django.urls import path
from .views import (
    WalkRewardRuleListCreateView,
    WalkRewardRuleDetailView,
    SubmitStepsView,
    MyWalkHistoryView,
)

urlpatterns = [
    # Admin
    path("admin/rules/", WalkRewardRuleListCreateView.as_view(), name="walk-rules"),
    path("admin/rules/<int:pk>/", WalkRewardRuleDetailView.as_view(), name="walk-rule-detail"),

    # User
    path("submit-steps/", SubmitStepsView.as_view(), name="submit-steps"),
    path("my-history/", MyWalkHistoryView.as_view(), name="my-walk-history"),
]
