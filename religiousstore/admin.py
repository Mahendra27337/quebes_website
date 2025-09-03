from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ReligiousStore

@admin.register(ReligiousStore)
class ReligiousStoreAdmin(admin.ModelAdmin):
    list_display = ("sku_id", "product_name", "vendor_name", "company_name", "product_inr_price", "inventory")
    search_fields = ("sku_id", "product_name", "vendor_name", "company_name")
    list_filter = ("category", "sub_category", "featured_offer", "sponsored_flag", "fraud_flag")
