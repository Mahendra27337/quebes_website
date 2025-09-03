from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from .models import PerformAndEarn, UserPerformTask
from .serializers import (
    PerformAndEarnSerializer,
    UserPerformTaskSerializer,
    PerformAndEarnDetailSerializer,
)

from milestones.models import UserMilestone, Milestone


# 🔹 List + Create Offers
class PerformAndEarnListCreateView(generics.ListCreateAPIView):
    queryset = PerformAndEarn.objects.all()
    serializer_class = PerformAndEarnSerializer


# 🔹 Single Offer CRUD
class PerformAndEarnDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PerformAndEarn.objects.all()
    serializer_class = PerformAndEarnSerializer


# 🔹 User starts a task
class UserPerformTaskCreateView(generics.CreateAPIView):
    serializer_class = UserPerformTaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# 🔹 User completes a task
class UserPerformTaskCompleteView(generics.UpdateAPIView):
    serializer_class = UserPerformTaskSerializer
    permission_classes = [IsAuthenticated]
    queryset = UserPerformTask.objects.all()

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        task.mark_completed()
        return Response(
            {"status": "Task completed and MLM payout distributed"},
            status=status.HTTP_200_OK,
        )


# 🔹 Vendor callback to mark milestone progress
@api_view(["POST"])
def milestone_callback(request):
    """
    Vendor callback → marks a milestone as completed for a user.
    Expected payload:
    {
        "user_id": 1,
        "milestone_id": 10,
        "status": "approved"
    }
    """
    user_id = request.data.get("user_id")
    milestone_id = request.data.get("milestone_id")
    status_value = request.data.get("status", "approved")

    try:
        user_milestone, created = UserMilestone.objects.get_or_create(
            user_id=user_id, milestone_id=milestone_id
        )
        user_milestone.status = status_value
        user_milestone.save()

        return Response(
            {"success": True, "message": f"Milestone {milestone_id} marked {status_value}"}
        )
    except Milestone.DoesNotExist:
        return Response(
            {"success": False, "error": "Invalid milestone"}, status=400
        )


# 🔹 Get full task details + milestone progress
@api_view(["GET"])
def perform_task_detail(request, task_id):
    """
    Get full PerformAndEarn details + milestone progress for logged-in user.
    """
    try:
        task = PerformAndEarn.objects.get(id=task_id)
    except PerformAndEarn.DoesNotExist:
        return Response({"error": "Task not found"}, status=404)

    serializer = PerformAndEarnDetailSerializer(task, context={"user": request.user})
    return Response(serializer.data)
