from django.contrib import admin
from .models import PerformAndEarn, UserPerformTask
from milestones.models import MilestoneSet, Milestone


# ========== Inline setup for Milestones ==========
class MilestoneInline(admin.TabularInline):
    model = Milestone
    extra = 1
    fields = ("title", "description", "order", "payout", "feedback_schema")


# ========== Inline setup for MilestoneSets ==========
class MilestoneSetAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    inlines = [MilestoneInline]


# Unregister first if already registered in milestones/admin.py
try:
    admin.site.unregister(MilestoneSet)
except admin.sites.NotRegistered:
    pass

admin.site.register(MilestoneSet, MilestoneSetAdmin)


# ========== PerformAndEarn ==========
@admin.register(PerformAndEarn)
class PerformAndEarnAdmin(admin.ModelAdmin):
    list_display = (
        "offer_name",
        "vendor_name",
        "company_name",
        "category",
        "task_payout_amount",
        "referral_payout",
    )
    search_fields = ("offer_name", "vendor_name", "company_name")
    filter_horizontal = ("milestone_sets",)  # 👈 allows attaching multiple sets


# ========== UserPerformTask ==========
@admin.register(UserPerformTask)
class UserPerformTaskAdmin(admin.ModelAdmin):
    list_display = ("user", "task", "status", "reward_credited", "created_at")
    list_filter = ("status",)







