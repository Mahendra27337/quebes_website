from django.db import models
from django.contrib.auth.models import User


class Referral(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="mlm_referral"
    )  # each user has MLM referral profile

    referred_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mlm_downlines",   # ✅ unique name
    )

    def __str__(self):
        return f"{self.user.username} referred by {self.referred_by.username if self.referred_by else 'None'}"


class ReferralIncome(models.Model):
    LEVEL_CHOICES = (
        (1, "Level 1 (40%)"),
        (2, "Level 2 (30%)"),
        (3, "Level 3 (30%)"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mlm_incomes")
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="mlm_generated_incomes"
    )
    level = models.IntegerField(choices=LEVEL_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} earned {self.amount} from {self.from_user.username} (L{self.level})"

