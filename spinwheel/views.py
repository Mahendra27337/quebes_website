from django.shortcuts import render

# Create your views here.
import random
from datetime import date

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SpinSegment, SpinHistory, SpinSettings
from .serializers import (
    SpinSegmentSerializer,
    SpinHistorySerializer,
    SpinSettingsSerializer,
)


# --- Admin endpoints ---

class SpinSegmentListCreateView(generics.ListCreateAPIView):
    """
    Admin: create/list segments.
    """
    queryset = SpinSegment.objects.all().order_by("id")
    serializer_class = SpinSegmentSerializer
    permission_classes = [IsAdminUser]


class SpinSettingsView(generics.RetrieveUpdateAPIView):
    """
    Admin: get/update global spin settings (singleton id=1).
    """
    queryset = SpinSettings.objects.all()
    serializer_class = SpinSettingsSerializer
    permission_classes = [IsAdminUser]

    def get_object(self):
        obj, _ = SpinSettings.objects.get_or_create(id=1)
        return obj


# --- Public/user endpoints ---

class PublicSegmentsView(generics.ListAPIView):
    """
    Optional: expose current configured segments (no auth).
    """
    queryset = SpinSegment.objects.all().order_by("id")
    serializer_class = SpinSegmentSerializer
    permission_classes = [AllowAny]


class SpinWheelView(APIView):
    """
    Auth user spins the wheel (enforces daily limit).
    Returns selected segment + remaining spins today + lifetime stats.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        segments = list(SpinSegment.objects.all())
        if not segments:
            return Response({"error": "No segments configured."}, status=400)

        settings, _ = SpinSettings.objects.get_or_create(id=1)
        daily_limit = settings.daily_limit

        today = date.today()
        spins_today = SpinHistory.objects.filter(user=request.user, created_at__date=today).count()
        if spins_today >= daily_limit:
            return Response(
                {"error": f"Daily spin limit reached ({daily_limit} spins allowed)."},
                status=403
            )

        # Weighted random selection
        choices = segments
        weights = [max(0.0, float(s.probability)) for s in segments]
        if sum(weights) <= 0:
            return Response({"error": "Invalid segment probabilities."}, status=400)

        selected_segment = random.choices(choices, weights=weights, k=1)[0]

        # Record spin
        SpinHistory.objects.create(user=request.user, segment=selected_segment)

        # Lifetime stats
        total_spins = SpinHistory.objects.filter(user=request.user).count()
        total_quebes = SpinHistory.objects.filter(user=request.user, segment__type="quebes").count()
        total_coupons = SpinHistory.objects.filter(user=request.user, segment__type="coupon").count()
        total_gift_cards = SpinHistory.objects.filter(user=request.user, segment__type="gift_card").count()

        return Response({
            "message": f"You got {selected_segment.name}!",
            "segment": SpinSegmentSerializer(selected_segment).data,
            "spins_left_today": max(0, daily_limit - (spins_today + 1)),
            "lifetime_stats": {
                "total_spins": total_spins,
                "total_quebes_won": total_quebes,
                "total_coupons_won": total_coupons,
                "total_gift_cards_won": total_gift_cards
            }
        }, status=200)


class SpinHistoryView(generics.ListAPIView):
    """
    Auth user: list my spin history, plus lifetime stats in the payload.
    """
    serializer_class = SpinHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SpinHistory.objects.filter(user=self.request.user).select_related("segment")

    def list(self, request, *args, **kwargs):
        resp = super().list(request, *args, **kwargs)

        total_spins = SpinHistory.objects.filter(user=request.user).count()
        total_quebes = SpinHistory.objects.filter(user=request.user, segment__type="quebes").count()
        total_coupons = SpinHistory.objects.filter(user=request.user, segment__type="coupon").count()
        total_gift_cards = SpinHistory.objects.filter(user=request.user, segment__type="gift_card").count()

        resp.data = {
            "history": resp.data,
            "lifetime_stats": {
                "total_spins": total_spins,
                "total_quebes_won": total_quebes,
                "total_coupons_won": total_coupons,
                "total_gift_cards_won": total_gift_cards
            }
        }
        return resp
