from django.db import models
from django.utils import timezone


class DigitalProduct(models.Model):
    sku_id = models.CharField(max_length=100, unique=True)
    product_name = models.CharField(max_length=255)
    vendor_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    brand_information = models.TextField(blank=True, null=True)
    sku_description = models.TextField(blank=True, null=True)
    milestone_name = models.CharField(max_length=255, blank=True, null=True)
    milestone_type = models.CharField(max_length=100, blank=True, null=True)
    milestone_description = models.TextField(blank=True, null=True)
    milestone_payout = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    terms_conditions = models.TextField(blank=True, null=True)
    how_to_earn = models.TextField(blank=True, null=True)
    whom_to_sell = models.TextField(blank=True, null=True)
    brand_logo = models.ImageField(upload_to='digitalstore/logos/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='digitalstore/banners/', blank=True, null=True)
    offer_video_file = models.FileField(upload_to='digitalstore/videos/', blank=True, null=True)
    offer_video_youtube = models.URLField(blank=True, null=True)
    referral_payout = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    share_and_earn_enabled = models.BooleanField(default=False)
    travel_required = models.BooleanField(default=False)
    category = models.CharField(max_length=255, blank=True, null=True)
    sub_category = models.CharField(max_length=255, blank=True, null=True)
    daily_task = models.BooleanField(default=False)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    credit_type = models.CharField(max_length=100, blank=True, null=True)
    tracking_type = models.CharField(max_length=100, blank=True, null=True)
    payout_info = models.TextField(blank=True, null=True)
    task_of_the_day = models.BooleanField(default=False)
    conversion_window_days = models.IntegerField(blank=True, null=True)
    available_to_level_1 = models.BooleanField(default=False)
    featured_offer = models.BooleanField(default=False)
    custom_cta_label = models.CharField(max_length=255, blank=True, null=True)
    smart_rank_score_filter = models.BooleanField(default=False)
    smart_rank_score = models.FloatField(blank=True, null=True)
    show_in_sections = models.BooleanField(default=False)
    link_to_contest = models.BooleanField(default=False)
    vendor_visibility = models.BooleanField(default=True)
    platform_type = models.CharField(max_length=50, blank=True, null=True)
    product_position_rank = models.IntegerField(blank=True, null=True)
    sponsored_flag = models.BooleanField(default=False)
    fraud_flag = models.BooleanField(default=False)
    success_ratio_req = models.FloatField(blank=True, null=True)
    geo_targeting = models.TextField(blank=True, null=True)
    user_targeting_tags = models.TextField(blank=True, null=True)
    click_behavior = models.CharField(max_length=100, blank=True, null=True)
    offer_wall = models.BooleanField(default=False)
    trigger_badge_unlock = models.BooleanField(default=False)
    review_module_for_app = models.BooleanField(default=False)
    my_lead = models.BooleanField(default=False)
    minimum_cart_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    carousel_image_1 = models.ImageField(upload_to='digitalstore/carousel/', blank=True, null=True)
    carousel_image_2 = models.ImageField(upload_to='digitalstore/carousel/', blank=True, null=True)
    carousel_image_3 = models.ImageField(upload_to='digitalstore/carousel/', blank=True, null=True)
    carousel_image_4 = models.ImageField(upload_to='digitalstore/carousel/', blank=True, null=True)
    product_inr_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    product_quebes_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    product_url = models.URLField(blank=True, null=True)
    enable_max_user = models.BooleanField(default=False)
    max_purchase_per_user = models.IntegerField(blank=True, null=True)
    inventory = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name


class DigitalPurchase(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    product = models.ForeignKey(DigitalProduct, on_delete=models.CASCADE)
    user_id = models.CharField(max_length=255)
    android_id = models.CharField(max_length=255, blank=True, null=True)
    imei_number = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    fraud_flag = models.BooleanField(default=False)
    postback_url = models.URLField(blank=True, null=True)
    callback_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Purchase #{self.id} - {self.product.product_name}"
