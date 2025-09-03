# performandearn/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from milestones.models import UserMilestone
from mlm.utils import distribute_referral_income

@receiver(post_save, sender=UserMilestone)
def handle_milestone_completion(sender, instance, created, **kwargs):
    """
    When a milestone is approved -> trigger MLM payout.
    """
    if instance.status == "approved":
        payout = instance.milestone.payout
        user = instance.user

        if payout > 0:
            distribute_referral_income(user, payout)
