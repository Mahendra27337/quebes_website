from django.urls import path
from .views import ReferralView, RegisterAPIView, LoginAPIView, TaskCreateAPIView, TaskListAPIView, OfferCompleteAPIView, ReferralHistoryAPIView
from .views import ContestCreateAPIView, ContestListAPIView, BannerCreateAPIView, BannerListAPIView
from .views import TaskCreateAPIView, TaskPostbackAPIView
urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('task/create/', TaskCreateAPIView.as_view()),
    path('task/list/', TaskListAPIView.as_view()),
    path('offer/complete/', OfferCompleteAPIView.as_view()),
    path('referral/history/<str:username>/', ReferralHistoryAPIView.as_view()),
    path('contest/create/', ContestCreateAPIView.as_view(), name='contest-create'),
    path('contest/list/', ContestListAPIView.as_view(), name='contest-list'),
    path('banner/create/', BannerCreateAPIView.as_view(), name='banner-create'),
    path('banner/list/', BannerListAPIView.as_view(), name='banner-list'),
      path('task/create/', TaskCreateAPIView.as_view(), name='task-create'),
    path('task/postback/', TaskPostbackAPIView.as_view(), name='task-postback'),
    path("referrals/", ReferralView.as_view(), name="referrals"),
]


