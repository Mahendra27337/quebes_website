from rest_framework import serializers
from .models import ShareAndEarnOffer, ShareAndEarnMilestone, Referral


class ShareAndEarnMilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareAndEarnMilestone
        fields = ["id", "milestone_name", "milestone_type", "milestone_description", "milestone_payout"]


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = ["id", "referrer_id", "referee_id", "level", "created_at"]


class ShareAndEarnOfferSerializer(serializers.ModelSerializer):
    milestones = ShareAndEarnMilestoneSerializer(many=True, required=False)
    referrals = ReferralSerializer(many=True, read_only=True)

    class Meta:
        model = ShareAndEarnOffer
        fields = "__all__"

    def create(self, validated_data):
        milestones_data = validated_data.pop("milestones", [])
        offer = ShareAndEarnOffer.objects.create(**validated_data)
        for milestone_data in milestones_data:
            ShareAndEarnMilestone.objects.create(offer=offer, **milestone_data)
        return offer

    def update(self, instance, validated_data):
        milestones_data = validated_data.pop("milestones", [])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if milestones_data:
            instance.milestones.all().delete()
            for milestone_data in milestones_data:
                ShareAndEarnMilestone.objects.create(offer=instance, **milestone_data)

        return instance
