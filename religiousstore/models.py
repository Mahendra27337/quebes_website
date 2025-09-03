from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth import get_user_model
from milestones.models import MilestoneSet  # reuse milestone sets

User = get_user_model()

class ReligiousStore(models.Model):
    sku_id = models.CharField(max_length=100, unique=True)
    product_name = models.CharField(max_length=255)
    vendor_name = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    brand_information = models.TextField(blank=True, null=True)
    sku_description = models.TextField(blank=True, null=True)

    # milestone linking
    milestone_set = models.ForeignKey(
        MilestoneSet, on_delete=models.SET_NULL, null=True, blank=True, related_name="religious_products"
    )

    terms_conditions = models.TextField(blank=True, null=True)
    how_to_earn = models.TextField(blank=True, null=True)
    whom_to_sell = models.TextField(blank=True, null=True)

    brand_logo = models.ImageField(upload_to="religiousstore/logos/", null=True, blank=True)
    banner_image = models.ImageField(upload_to="religiousstore/banners/", null=True, blank=True)
    offer_video_file = models.FileField(upload_to="religiousstore/videos/", null=True, blank=True)
    offer_video_youtube = models.URLField(blank=True, null=True)

    referral_payout = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    share_earn_enabled = models.BooleanField(default=False)
    travel_required = models.BooleanField(default=False)

    category = models.CharField(max_length=100, blank=True, null=True)
    sub_category = models.CharField(max_length=100, blank=True, null=True)
    daily_task = models.TextField(blank=True, null=True)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    credit_type = models.CharField(max_length=100, blank=True, null=True)
    tracking_type = models.CharField(max_length=100, blank=True, null=True)

    religious_store_payout_info = models.TextField(blank=True, null=True)
    task_of_the_day = models.TextField(blank=True, null=True)
    conversion_window_days = models.IntegerField(default=0)

    available_to_level1 = models.BooleanField(default=True)
    featured_offer = models.BooleanField(default=False)
    custom_cta_label = models.CharField(max_length=255, blank=True, null=True)

    smart_rank_score_filter = models.BooleanField(default=False)
    smart_rank_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    show_in_sections = models.BooleanField(default=True)
    link_to_contest = models.URLField(blank=True, null=True)
    vendor_visibility = models.BooleanField(default=True)
    platform_type = models.CharField(max_length=100, blank=True, null=True)
    product_position_rank = models.IntegerField(default=0)
    sponsored_flag = models.BooleanField(default=False)
    fraud_flag = models.BooleanField(default=False)

    success_ratio_req = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    geo_targeting = models.TextField(blank=True, null=True)
    user_targeting_tags = models.JSONField(blank=True, null=True)
    click_behavior = models.CharField(max_length=100, blank=True, null=True)
    offer_wall = models.BooleanField(default=False)

    trigger_badge_unlock = models.BooleanField(default=False)
    review_required = models.BooleanField(default=False)
    review_module = models.TextField(blank=True, null=True)
    my_lead = models.TextField(blank=True, null=True)

    min_cart_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    carousel_images = models.JSONField(blank=True, null=True)  # store up to 4 URLs

    product_inr_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    product_quebes_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    enable_max_user = models.BooleanField(default=False)
    max_purchase_per_user = models.IntegerField(default=0)

    inventory = models.IntegerField(default=0)
    credited_at = models.DateTimeField(auto_now_add=True)

    tiered_delivery = models.BooleanField(default=False)
    tiered_delivery_free = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tiered_delivery_basic = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tiered_delivery_pro = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tiered_delivery_premium = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    delivery_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    product_actual_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_quantity = models.CharField(max_length=100, blank=True, null=True)

    how_to_use = models.TextField(blank=True, null=True)
    ingredients = models.TextField(blank=True, null=True)
    key_benefits = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    trust_badge = models.TextField(blank=True, null=True)
    product_review = models.TextField(blank=True, null=True)
    feedback_module = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.product_name} ({self.sku_id})"
