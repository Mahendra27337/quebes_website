from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from decimal import Decimal

from mlm.utils import distribute_referral_income  

User = get_user_model()

MILESTONE_STATUS = (
    ("locked", "Locked"),
    ("in_review", "In Review"),
    ("approved", "Approved"),
    ("rejected", "Rejected"),
)


class MilestoneSet(models.Model):
    """
    A reusable set of milestones that can be attached to:
    - Perform & Earn task (direct FK)
    - Any other model (via GenericForeignKey)
    """
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ Corrected: link to PerformAndEarn instead of missing PerformTask
class MilestoneSet(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    perform_task = models.ForeignKey(
        "performandearn.PerformAndEarn",
        null=True,
        blank=True,
        related_name="perform_milestone_sets",  # ✅ renamed to avoid clash
        on_delete=models.CASCADE
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey("content_type", "object_id")

class Meta:
        verbose_name = "Milestone Set"
        verbose_name_plural = "Milestone Sets"

def __str__(self):
        return self.name

def first_milestone(self):
        return self.milestones.order_by("order").first()


class Milestone(models.Model):
    milestone_set = models.ForeignKey(MilestoneSet, related_name="milestones", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)
    payout = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    feedback_schema = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ["order"]
        unique_together = ("milestone_set", "order")

    def __str__(self):
        return f"{self.milestone_set.name} → {self.title} (#{self.order})"


class UserMilestone(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_milestones")
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, related_name="user_milestones")

    status = models.CharField(max_length=20, choices=MILESTONE_STATUS, default="locked")
    screenshot = models.ImageField(upload_to="milestones/screenshots/", null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    feedback_answers = models.JSONField(null=True, blank=True)

    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    admin_comment = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "milestone")

    def __str__(self):
        return f"{self.user} → {self.milestone} [{self.status}]"

    def approve(self, admin_user=None, comment=None):
        self.status = "approved"
        self.reviewed_at = timezone.now()
        if comment:
            self.admin_comment = comment
        self.save()

        if self.milestone.payout > 0:
            distribute_referral_income(self.user, Decimal(self.milestone.payout))




