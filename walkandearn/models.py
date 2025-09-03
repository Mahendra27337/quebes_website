from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class WalkRewardRule(models.Model):
    REWARD_TYPES = [
        ("coupon", "Coupon"),
        ("gift_card", "Gift Card"),
        ("quebes", "Quebes"),
        ("discount", "Discount"),
        ("trial_product", "Trial Product"),
        ("other", "Other"),
    ]

    day = models.IntegerField(help_text="Day number in challenge (1..30 etc.)")
    min_steps = models.IntegerField()
    max_steps = models.IntegerField(blank=True, null=True)  # if No Limit keep NULL
    name = models.CharField(max_length=200)

    reward_type = models.CharField(max_length=50, choices=REWARD_TYPES)
    reward_section = models.CharField(max_length=200, blank=True, null=True)
    reward_category = models.CharField(max_length=200, blank=True, null=True)
    reward_offer = models.CharField(max_length=200, blank=True, null=True)
    reward_value = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Ex: 20% OFF, 5 Quebes, Free Trial Product"
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("day",)

    def __str__(self):
        return f"Day {self.day} - {self.name}"


class WalkHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.IntegerField()
    steps = models.IntegerField()
    reward_unlocked = models.BooleanField(default=False)
    reward_value = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("user", "day")  # one entry per user per day

    def __str__(self):
        return f"{self.user.username} - Day {self.day} - Steps {self.steps}"
