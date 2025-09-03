from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class SpinSegment(models.Model):
    SEGMENT_TYPES = [
        ("try_again", "Try Again"),
        ("coupon", "Coupon"),
        ("quebes", "Quebes"),
        ("gift_card", "Gift Card"),
    ]

    name = models.CharField(max_length=100)
    probability = models.FloatField(help_text="Probability percentage (all segments should sum to ~100)")
    type = models.CharField(max_length=20, choices=SEGMENT_TYPES)
    link_section = models.CharField(max_length=200, blank=True, null=True)
    link_category = models.CharField(max_length=200, blank=True, null=True)
    link_offer = models.CharField(max_length=200, blank=True, null=True)
    # e.g. for quebes -> "5"; for coupon -> "SAVE20"; for gift_card -> "₹100 Amazon"
    reward_value = models.CharField(max_length=200, blank=True, null=True, help_text="Quebes count / Coupon code / Gift info")

    def __str__(self):
        return f"{self.name} ({self.type})"


class SpinHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    segment = models.ForeignKey(SpinSegment, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        seg = self.segment.name if self.segment else "Unknown"
        return f"{self.user.username} -> {seg} @ {self.created_at.isoformat()}"


class SpinSettings(models.Model):
    # global singleton settings (id=1)
    daily_limit = models.PositiveIntegerField(default=1, help_text="Max spins allowed per user per day")

    def __str__(self):
        return f"Spin Settings (Daily Limit: {self.daily_limit})"
