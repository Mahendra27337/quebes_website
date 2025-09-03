from rest_framework import serializers
from .models import SpinSegment, SpinHistory, SpinSettings


class SpinSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpinSegment
        fields = "__all__"


class SpinHistorySerializer(serializers.ModelSerializer):
    segment = SpinSegmentSerializer()

    class Meta:
        model = SpinHistory
        fields = ["id", "segment", "created_at"]


class SpinSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpinSettings
        fields = ["id", "daily_limit"]
