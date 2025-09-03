from django.contrib import admin
from .models import DigitalProduct, DigitalPurchase


@admin.register(DigitalProduct)
class DigitalProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku_id', 'product_name', 'vendor_name', 'company_name',
        'category', 'sub_category', 'fraud_flag', 'featured_offer',
        'sponsored_flag', 'created_at'
    )
    list_filter = ('category', 'sub_category', 'fraud_flag', 'featured_offer', 'sponsored_flag')
    search_fields = ('sku_id', 'product_name', 'vendor_name', 'company_name')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(DigitalPurchase)
class DigitalPurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user_id', 'status', 'fraud_flag', 'created_at')
    list_filter = ('status', 'fraud_flag')
    search_fields = ('user_id', 'product__product_name', 'android_id', 'imei_number')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
