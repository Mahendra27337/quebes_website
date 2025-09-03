from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Banner, Contest, UserProfile, Task, ReferralIncome
import uuid


# ---------------- USER PROFILE ---------------- #
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    referral_code = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = UserProfile
        exclude = ['id', 'user']  # keep user internal

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        referral_code = validated_data.pop('referral_code', None)

        # 1️⃣ Create User
        user = User.objects.create_user(username=username, password=password)

        # 2️⃣ Create Profile (auto-generate referral_code if missing)
        profile = UserProfile.objects.create(
            user=user,
            referral_code=str(uuid.uuid4().hex[:8].upper()),  # unique code
            **validated_data
        )

        # 3️⃣ Handle Referral Linking
        if referral_code:
            try:
                referrer_profile = UserProfile.objects.get(referral_code=referral_code)
                profile.referral_by = referrer_profile.user
                profile.save()
            except UserProfile.DoesNotExist:
                pass  # invalid referral code → ignore

        return profile


# ---------------- REFERRAL SERIALIZERS ---------------- #
class ReferredUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["name", "email", "referral_code"]


class ReferralSerializer(serializers.ModelSerializer):
    referred_users = serializers.SerializerMethodField()
    referrer = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ["referral_code", "referrer", "referred_users"]

    def get_referred_users(self, obj):
        referred_profiles = UserProfile.objects.filter(referral_by=obj.user)
        return ReferredUserSerializer(referred_profiles, many=True).data

    def get_referrer(self, obj):
        if obj.referral_by:
            return obj.referral_by.username
        return None



class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class ReferralIncomeSerializer(serializers.ModelSerializer):
    referred_user = serializers.StringRelatedField()
    class Meta:
        model = ReferralIncome
        fields = '__all__'


class ContestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contest
        fields = '__all__'

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'