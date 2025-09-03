from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import ScratchCard, ScratchCardHistory
from .serializers import ScratchCardSerializer, ScratchCardHistorySerializer


# --- Admin Endpoints ---

class ScratchCardListCreateView(generics.ListCreateAPIView):
    """
    Admin: Create / List all scratch cards
    """
    queryset = ScratchCard.objects.all().order_by("id")
    serializer_class = ScratchCardSerializer
    permission_classes = [IsAdminUser]


class ScratchCardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Admin: Retrieve / Update / Delete a scratch card
    """
    queryset = ScratchCard.objects.all()
    serializer_class = ScratchCardSerializer
    permission_classes = [IsAdminUser]


# --- User Endpoints ---

class UserScratchCardsView(generics.ListAPIView):
    """
    List scratch cards assigned to the user (active & not yet scratched).
    """
    serializer_class = ScratchCardHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ScratchCardHistory.objects.filter(user=self.request.user)


class ScratchCardScratchView(APIView):
    """
    User scratches the card -> reward revealed.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            history = ScratchCardHistory.objects.get(id=pk, user=request.user)
        except ScratchCardHistory.DoesNotExist:
            return Response({"error": "Scratch card not found for user."}, status=404)

        if history.is_scratched:
            return Response({"error": "Scratch card already scratched."}, status=400)

        # Reveal reward
        history.is_scratched = True
        history.reward_revealed = history.card.reward_value
        history.save()

        return Response({
            "message": f"Congrats! You revealed: {history.reward_revealed}",
            "scratch_card": ScratchCardHistorySerializer(history).data
        }, status=200)
