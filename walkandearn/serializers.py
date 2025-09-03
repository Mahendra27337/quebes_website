from rest_framework import serializers
from .models import WalkRewardRule, WalkHistory


class WalkRewardRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalkRewardRule
        fields = "__all__"


class WalkHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WalkHistory
        fields = ["id", "day", "steps", "reward_unlocked", "reward_value", "created_at"]
