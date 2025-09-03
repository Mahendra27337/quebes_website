from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class ScratchCard(models.Model):
    REWARD_TYPES = [
        ("discount", "Discount"),
        ("quebes", "Quebes"),
        ("product", "Trial Product"),
        ("coupon", "Coupon"),
        ("gift_card", "Gift Card"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=100)
    # To define when this scratch card should appear
    trigger_section = models.CharField(max_length=200, blank=True, null=True)
    trigger_category = models.CharField(max_length=200, blank=True, null=True)
    trigger_offer = models.CharField(max_length=200, blank=True, null=True)

    # Reward configuration
    reward_type = models.CharField(max_length=50, choices=REWARD_TYPES)
    reward_section = models.CharField(max_length=200, blank=True, null=True)
    reward_category = models.CharField(max_length=200, blank=True, null=True)
    reward_offer = models.CharField(max_length=200, blank=True, null=True)
    reward_value = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text="Ex: 20% OFF, 5 Quebes, Free Trial Product, Coupon Code"
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ScratchCardHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(ScratchCard, on_delete=models.CASCADE)
    is_scratched = models.BooleanField(default=False)
    reward_revealed = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user.username} - {self.card.name} - {'Scratched' if self.is_scratched else 'Pending'}"
