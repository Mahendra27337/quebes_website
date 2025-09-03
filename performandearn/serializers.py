from rest_framework import serializers
from .models import PerformAndEarn, UserPerformTask
from milestones.models import Milestone, MilestoneSet, UserMilestone


# 🔹 Main PerformAndEarn Serializer
class PerformAndEarnSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformAndEarn
        fields = "__all__"


# 🔹 User’s task participation
class UserPerformTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPerformTask
        fields = "__all__"


# 🔹 Milestone Serializer
class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = ["id", "title", "description", "order", "payout", "feedback_schema"]


# 🔹 PerformAndEarn with milestones
class PerformAndEarnWithMilestonesSerializer(serializers.ModelSerializer):
    milestones = serializers.SerializerMethodField()

    class Meta:
        model = PerformAndEarn
        fields = "__all__"

    def get_milestones(self, obj):
        if obj.milestone_set:
            return MilestoneSerializer(obj.milestone_set.milestones.all(), many=True).data
        return []


# 🔹 Track user’s milestone progress
class MilestoneProgressSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Milestone
        fields = ["id", "title", "description", "order", "payout", "status"]

    def get_status(self, obj):
        user = self.context.get("user")
        if not user or user.is_anonymous:
            return "locked"
        try:
            user_milestone = UserMilestone.objects.get(user=user, milestone=obj)
            return user_milestone.status
        except UserMilestone.DoesNotExist:
            return "locked"


# 🔹 Detailed PerformAndEarn serializer (for frontend display)
class PerformAndEarnDetailSerializer(serializers.ModelSerializer):
    milestones = serializers.SerializerMethodField()

    class Meta:
        model = PerformAndEarn
        fields = [
            "id",
            "offer_name",
            "vendor_name",
            "company_name",
            "offer_brand_info",
            "offer_brand_benefits",
            "terms_conditions",
            "task_payout_amount",
            "referral_payout",
            "pe_offer_link",
            "share_and_earn_enabled",
            "category",
            "sub_category",
            "start_date",
            "end_date",
            "featured_partner",
            "platform_type",
            "fraud_flag",
            "sponsored_flag",
            "success_ratio_required",
            "milestones",
        ]

    def get_milestones(self, obj):
        if obj.milestone_set:
            return MilestoneProgressSerializer(
                obj.milestone_set.milestones.all(),
                many=True,
                context=self.context,
            ).data
        return []
