from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import WalkRewardRule, WalkHistory
from .serializers import WalkRewardRuleSerializer, WalkHistorySerializer


# -------- ADMIN APIs ---------

class WalkRewardRuleListCreateView(generics.ListCreateAPIView):
    """Admin: Add daily walk reward rules"""
    queryset = WalkRewardRule.objects.all()
    serializer_class = WalkRewardRuleSerializer
    permission_classes = [IsAdminUser]


class WalkRewardRuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Admin: Update / Delete walk reward rule"""
    queryset = WalkRewardRule.objects.all()
    serializer_class = WalkRewardRuleSerializer
    permission_classes = [IsAdminUser]


# -------- USER APIs ---------

class SubmitStepsView(APIView):
    """User submits their daily steps and system checks rewards"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        day = request.data.get("day")
        steps = int(request.data.get("steps", 0))

        if not day or steps <= 0:
            return Response({"error": "Day and steps are required."}, status=400)

        # Check if entry exists
        if WalkHistory.objects.filter(user=user, day=day).exists():
            return Response({"error": "Steps already submitted for this day."}, status=400)

        # Find matching rule
        try:
            rule = WalkRewardRule.objects.get(day=day, is_active=True)
        except WalkRewardRule.DoesNotExist:
            return Response({"error": "No reward rule for this day."}, status=404)

        reward_unlocked = False
        reward_value = None

        if steps >= rule.min_steps and (rule.max_steps is None or steps <= rule.max_steps):
            reward_unlocked = True
            reward_value = rule.reward_value

        history = WalkHistory.objects.create(
            user=user,
            day=day,
            steps=steps,
            reward_unlocked=reward_unlocked,
            reward_value=reward_value
        )

        return Response({
            "message": "Steps submitted successfully",
            "history": WalkHistorySerializer(history).data,
            "reward": reward_value if reward_unlocked else "No reward earned"
        }, status=201)


class MyWalkHistoryView(generics.ListAPIView):
    """User fetches their walk history"""
    serializer_class = WalkHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return WalkHistory.objects.filter(user=self.request.user)
