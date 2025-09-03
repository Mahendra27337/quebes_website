from django.contrib import admin
from django.utils.html import format_html
from .models import BrandStore, BrandStoreMilestone


class BrandStoreMilestoneInline(admin.TabularInline):
    model = BrandStoreMilestone
    extra = 1


@admin.register(BrandStore)
class BrandStoreAdmin(admin.ModelAdmin):
    list_display = (
        "brand_store_id",
        "store_offer_name",
        "vendor_name",
        "company_name",
        "brand_store_task_payout",
        "brand_store_referral_payout",
        "featured_offer",
        "brand_store_category",
        "brand_store_sub_category",
        "start_date",
        "end_date",
        "brand_logo_preview",  # ✅ method inside admin
    )

    search_fields = (
        "store_offer_name",
        "vendor_name",
        "company_name",
        "brand_store_category",
        "brand_store_sub_category",
    )

    list_filter = (
        "featured_offer",
        "available_to_il1",
        "brand_store_category",
        "brand_store_sub_category",
        "start_date",
        "end_date",
    )

    date_hierarchy = "start_date"
    ordering = ("-start_date",)

    readonly_fields = (
        "brand_logo_preview",
        "banner_image_preview",
        "carousel_image_1_preview",
        "carousel_image_2_preview",
        "carousel_image_3_preview",
        "carousel_image_4_preview",
    )

    inlines = [BrandStoreMilestoneInline]

    # ✅ Preview methods MUST be defined inside this class
    def brand_logo_preview(self, obj):
        if obj.brand_logo:
            return format_html('<img src="{}" width="80" height="80" style="object-fit:contain;" />', obj.brand_logo.url)
        return "No Logo"
    brand_logo_preview.short_description = "Logo"

    def banner_image_preview(self, obj):
        if obj.banner_image:
            return format_html('<img src="{}" width="150" height="60" style="object-fit:contain;" />', obj.banner_image.url)
        return "No Banner"
    banner_image_preview.short_description = "Banner"

    def carousel_image_1_preview(self, obj):
        if obj.carousel_image_1:
            return format_html('<img src="{}" width="100" height="60" style="object-fit:contain;" />', obj.carousel_image_1.url)
        return "No Image"

    def carousel_image_2_preview(self, obj):
        if obj.carousel_image_2:
            return format_html('<img src="{}" width="100" height="60" style="object-fit:contain;" />', obj.carousel_image_2.url)
        return "No Image"

    def carousel_image_3_preview(self, obj):
        if obj.carousel_image_3:
            return format_html('<img src="{}" width="100" height="60" style="object-fit:contain;" />', obj.carousel_image_3.url)
        return "No Image"

    def carousel_image_4_preview(self, obj):
        if obj.carousel_image_4:
            return format_html('<img src="{}" width="100" height="60" style="object-fit:contain;" />', obj.carousel_image_4.url)
        return "No Image"

