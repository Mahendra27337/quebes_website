from django.urls import path
from .views import CreateReferralAPIView, DistributeIncomeAPIView, UserIncomeListAPIView

urlpatterns = [
    path("create-referral/", CreateReferralAPIView.as_view(), name="create-referral"),
    path("distribute-income/", DistributeIncomeAPIView.as_view(), name="distribute-income"),
    path("user-incomes/<int:user_id>/", UserIncomeListAPIView.as_view(), name="user-incomes"),
]
