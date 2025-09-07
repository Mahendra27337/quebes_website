from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ShareAndEarnOffer, ShareAndEarnMilestone, Referral


class ShareAndEarnMilestoneInline(admin.TabularInline):
    model = ShareAndEarnMilestone
    extra = 1


@admin.register(ShareAndEarnOffer)
class ShareAndEarnOfferAdmin(admin.ModelAdmin):
    list_display = ("yes_id", "offer_name_se", "vendor_name", "company_name", "category", "fraud_flag", "sponsored_flag", "created_at")
    search_fields = ("yes_id", "offer_name_se", "vendor_name", "company_name")
    list_filter = ("category", "fraud_flag", "sponsored_flag", "featured_partner")
    inlines = [ShareAndEarnMilestoneInline]
    ordering = ("-created_at",)


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ("offer", "referrer_id", "referee_id", "level", "created_at")
    search_fields = ("referrer_id", "referee_id", "offer__offer_name_se")
    list_filter = ("level", "created_at")
    ordering = ("-created_at",)
