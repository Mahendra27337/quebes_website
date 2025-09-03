from decimal import Decimal
from django.contrib.auth.models import User
from .models import Referral, ReferralIncome


# Income distribution percentages
MLM_LEVELS = {
    1: Decimal("0.40"),  # 40%
    2: Decimal("0.30"),  # 30%
    3: Decimal("0.30"),  # 30%
}


def distribute_referral_income(from_user: User, total_amount: Decimal):
    """
    Distribute income when `from_user` earns `total_amount`.
    Income flows up to 3 levels (40% - 30% - 30%).
    """

    current_user = from_user
    for level in range(1, 4):
        try:
            referral = Referral.objects.get(user=current_user)
        except Referral.DoesNotExist:
            break

        sponsor = referral.referred_by
        if not sponsor:
            break

        percentage = MLM_LEVELS[level]
        reward_amount = total_amount * percentage

        ReferralIncome.objects.create(
            user=sponsor,
            from_user=from_user,
            level=level,
            amount=reward_amount,
        )

        # Move up one level for next iteration
        current_user = sponsor

