from rest_framework import serializers
from .models import (
    TrialVendor, TrialProduct, TrialProductCarousel,
    TrialProductMilestone, TrialStoreAd, TrialStoreFeedback
)


class TrialVendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrialVendor
        fields = "__all__"


class TrialProductCarouselSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrialProductCarousel
        fields = "__all__"


class TrialProductMilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrialProductMilestone
        fields = "__all__"


class TrialStoreAdSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrialStoreAd
        fields = "__all__"


class TrialStoreFeedbackSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TrialStoreFeedback
        fields = "__all__"


class TrialProductSerializer(serializers.ModelSerializer):
    vendor = TrialVendorSerializer(read_only=True)
    milestones = TrialProductMilestoneSerializer(many=True, read_only=True)
    carousel_images = TrialProductCarouselSerializer(many=True, read_only=True)
    feedbacks = TrialStoreFeedbackSerializer(many=True, read_only=True)

    class Meta:
        model = TrialProduct
        fields = "__all__"

from rest_framework import serializers
from .models import TrialAd, AdImpression, AdClick

class TrialAdSerializer(serializers.ModelSerializer):
    effective_cpm = serializers.ReadOnlyField()
    effective_cpc = serializers.ReadOnlyField()

    class Meta:
        model = TrialAd
        fields = "__all__"


class AdImpressionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdImpression
        fields = "__all__"


class AdClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdClick
        fields = "__all__"


