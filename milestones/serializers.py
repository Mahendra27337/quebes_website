from rest_framework import serializers
from .models import MilestoneSet, Milestone, UserMilestone


class MilestoneSerializer(serializers.ModelSerializer):
    """Serializer for a single milestone"""
    class Meta:
        model = Milestone
        fields = ["id", "title", "description", "order", "payout", "feedback_schema"]


class MilestoneSetSerializer(serializers.ModelSerializer):
    """Serializer for a set of milestones, includes nested milestone creation/updating"""
    milestones = MilestoneSerializer(many=True)

    class Meta:
        model = MilestoneSet
        fields = ["id", "name", "description", "perform_task", "milestones"]

    def create(self, validated_data):
        milestones_data = validated_data.pop("milestones", [])
        milestone_set = MilestoneSet.objects.create(**validated_data)
        for milestone in milestones_data:
            Milestone.objects.create(milestone_set=milestone_set, **milestone)
        return milestone_set

    def update(self, instance, validated_data):
        milestones_data = validated_data.pop("milestones", [])
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.perform_task = validated_data.get("perform_task", instance.perform_task)
        instance.save()

        # Replace old milestones with new ones
        instance.milestones.all().delete()
        for milestone in milestones_data:
            Milestone.objects.create(milestone_set=instance, **milestone)

        return instance


class UserMilestoneSerializer(serializers.ModelSerializer):
    """Serializer for user’s milestone progress"""
    milestone = MilestoneSerializer(read_only=True)

    class Meta:
        model = UserMilestone
        fields = "__all__"


class UserMilestoneApproveSerializer(serializers.ModelSerializer):
    """
    Serializer for admin approving/rejecting a milestone.
    Automatically calls `approve()` method if approved.
    """
    class Meta:
        model = UserMilestone
        fields = ["id", "status", "admin_comment"]

    def update(self, instance, validated_data):
        status = validated_data.get("status")
        comment = validated_data.get("admin_comment")

        if status == "approved":
            instance.approve(admin_user=self.context["request"].user, comment=comment)
        else:
            instance.status = status
            instance.admin_comment = comment
            instance.save()

        return instance
