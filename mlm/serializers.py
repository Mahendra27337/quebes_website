from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Referral, ReferralIncome


class ReferralSerializer(serializers.ModelSerializer):
    referred_by = serializers.StringRelatedField()

    class Meta:
        model = Referral
        fields = ["id", "user", "referred_by"]


class ReferralIncomeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    from_user = serializers.StringRelatedField()

    class Meta:
        model = ReferralIncome
        fields = ["id", "user", "from_user", "level", "amount", "created_at"]

