from rest_framework import serializers
from .models import ScratchCard, ScratchCardHistory


class ScratchCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScratchCard
        fields = "__all__"


class ScratchCardHistorySerializer(serializers.ModelSerializer):
    card = ScratchCardSerializer()

    class Meta:
        model = ScratchCardHistory
        fields = ["id", "card", "is_scratched", "reward_revealed", "created_at"]
