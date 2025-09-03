from django.contrib import admin
from .models import (
    TrialVendor, TrialProduct, TrialProductCarousel,
    TrialProductMilestone, TrialStoreAd, TrialStoreFeedback
)


@admin.register(TrialVendor)
class TrialVendorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "vendor_type", "subscription_fee", "created_at")
    list_filter = ("vendor_type",)
    search_fields = ("name", "company_name")


class TrialProductCarouselInline(admin.TabularInline):
    model = TrialProductCarousel
    extra = 1


class TrialProductMilestoneInline(admin.TabularInline):
    model = TrialProductMilestone
    extra = 1


@admin.register(TrialProduct)
class TrialProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "sku_id", "vendor", "product_inr_price", "inventory", "sponsored_flag", "fraud_flag")
    list_filter = ("category", "featured_offer", "sponsored_flag", "fraud_flag")
    search_fields = ("product_name", "sku_id", "vendor__name")
    inlines = [TrialProductCarouselInline, TrialProductMilestoneInline]


@admin.register(TrialStoreAd)
class TrialStoreAdAdmin(admin.ModelAdmin):
    list_display = ("id", "ad_name", "is_active")
    list_filter = ("is_active",)


@admin.register(TrialStoreFeedback)
class TrialStoreFeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("product__product_name", "user__username")
from django.contrib import admin
from .models import TrialAd, AdImpression, AdClick

@admin.register(TrialAd)
class TrialAdAdmin(admin.ModelAdmin):
    list_display = ("title", "ad_type", "cpm_rate", "cpc_rate", "boost_percentage", "frequency_cap", "active", "created_at")
    list_filter = ("ad_type", "active")
    search_fields = ("title", "advertiser")

@admin.register(AdImpression)
class AdImpressionAdmin(admin.ModelAdmin):
    list_display = ("ad", "user", "count", "last_seen")

@admin.register(AdClick)
class AdClickAdmin(admin.ModelAdmin):
    list_display = ("ad", "user", "timestamp")

