from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ScratchCard, ScratchCardHistory


@admin.register(ScratchCard)
class ScratchCardAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "reward_type", "reward_value", "is_active")
    list_filter = ("reward_type", "is_active")
    search_fields = ("name", "reward_value")


@admin.register(ScratchCardHistory)
class ScratchCardHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "card", "is_scratched", "reward_revealed", "created_at")
    list_filter = ("is_scratched", "created_at")
    search_fields = ("user__username", "card__name", "reward_revealed")
