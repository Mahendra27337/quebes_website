from django.urls import path
from .views import (
    ScratchCardListCreateView,
    ScratchCardDetailView,
    UserScratchCardsView,
    ScratchCardScratchView,
)

urlpatterns = [
    # Admin
    path("admin/cards/", ScratchCardListCreateView.as_view(), name="admin-scratchcards"),
    path("admin/cards/<int:pk>/", ScratchCardDetailView.as_view(), name="admin-scratchcard-detail"),

    # User
    path("my-cards/", UserScratchCardsView.as_view(), name="user-scratchcards"),
    path("scratch/<int:pk>/", ScratchCardScratchView.as_view(), name="scratch-card"),
]
