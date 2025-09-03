from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import WalkRewardRule, WalkHistory


@admin.register(WalkRewardRule)
class WalkRewardRuleAdmin(admin.ModelAdmin):
    list_display = ("id", "day", "min_steps", "max_steps", "reward_type", "reward_value", "is_active")
    list_filter = ("reward_type", "is_active")
    search_fields = ("name", "reward_value")


@admin.register(WalkHistory)
class WalkHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "day", "steps", "reward_unlocked", "reward_value", "created_at")
    list_filter = ("reward_unlocked", "created_at")
    search_fields = ("user__username", "reward_value")
