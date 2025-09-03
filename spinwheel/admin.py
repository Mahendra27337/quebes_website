from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import SpinSegment, SpinHistory, SpinSettings


@admin.register(SpinSegment)
class SpinSegmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "probability", "reward_value")
    list_filter = ("type",)
    search_fields = ("name", "reward_value")


@admin.register(SpinHistory)
class SpinHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "segment", "created_at")
    search_fields = ("user__username", "segment__name")
    list_filter = ("created_at",)


@admin.register(SpinSettings)
class SpinSettingsAdmin(admin.ModelAdmin):
    list_display = ("id", "daily_limit")
