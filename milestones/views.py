from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import MilestoneSet, Milestone, UserMilestone
from .serializers import (
    MilestoneSetSerializer,
    MilestoneSerializer,
    UserMilestoneSerializer,
    UserMilestoneApproveSerializer,
)


class MilestoneSetViewSet(viewsets.ModelViewSet):
    """CRUD for milestone sets (Admin only)"""
    queryset = MilestoneSet.objects.all()
    serializer_class = MilestoneSetSerializer
    permission_classes = [permissions.IsAdminUser]


class MilestoneViewSet(viewsets.ModelViewSet):
    """CRUD for individual milestones (Admin only)"""
    queryset = Milestone.objects.all()
    serializer_class = MilestoneSerializer
    permission_classes = [permissions.IsAdminUser]


class UserMilestoneViewSet(viewsets.ModelViewSet):
    """Tracks user progress on milestones"""
    queryset = UserMilestone.objects.all()
    serializer_class = UserMilestoneSerializer

    def get_permissions(self):
        if self.action in ["approve", "destroy"]:
            # Only admins can approve/reject or delete
            return [permissions.IsAdminUser()]
        elif self.action in ["create", "list", "retrieve", "update", "partial_update"]:
            # Authenticated users can create/update their own submissions
            return [permissions.IsAuthenticated()]
        return super().get_permissions()

    def get_queryset(self):
        """Users only see their own milestones; Admin sees all"""
        user = self.request.user
        if user.is_staff:
            return UserMilestone.objects.all()
        return UserMilestone.objects.filter(user=user)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        """
        Custom admin action: approve or reject a milestone
        Expected payload:
        {
            "status": "approved" | "rejected",
            "admin_comment": "optional text"
        }
        """
        milestone = self.get_object()
        serializer = UserMilestoneApproveSerializer(
            milestone, data=request.data, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
