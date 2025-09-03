from django.db import models
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

# Vendor Model
class TrialVendor(models.Model):
    VENDOR_TYPE_CHOICES = [
        ("free", "Free"),
        ("paid", "Paid"),
    ]
    name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    vendor_type = models.CharField(max_length=20, choices=VENDOR_TYPE_CHOICES, default="free")
    subscription_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Admin decides
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.vendor_type})"


# Trial Store Product
class TrialProduct(models.Model):
    sku_id = models.CharField(max_length=100, unique=True)
    product_name = models.CharField(max_length=255)
    vendor = models.ForeignKey(TrialVendor, on_delete=models.CASCADE, related_name="trial_products")
    company_name = models.CharField(max_length=255, blank=True, null=True)
    brand_information = models.TextField(blank=True, null=True)
    sku_description = models.TextField(blank=True, null=True)

    # Offer Media
    brand_logo = models.ImageField(upload_to="trialstore/logos/", blank=True, null=True)
    banner_image = models.ImageField(upload_to="trialstore/banners/", blank=True, null=True)
    offer_video_file = models.FileField(upload_to="trialstore/videos/", blank=True, null=True)
    offer_video_youtube = models.URLField(blank=True, null=True)

    # Offer Details
    trial_store_referral_payout = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    share_and_earn_enabled = models.BooleanField(default=False)
    travel_required = models.BooleanField(default=False)
    category = models.CharField(max_length=100, blank=True, null=True)
    sub_category = models.CharField(max_length=100, blank=True, null=True)
    daily_task = models.BooleanField(default=False)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    credit_type = models.CharField(max_length=100, blank=True, null=True)
    tracking_type = models.CharField(max_length=100, blank=True, null=True)
    trial_store_payout_info = models.TextField(blank=True, null=True)
    task_of_the_day = models.BooleanField(default=False)

    # Smart Rank
    smart_rank_score_filter = models.BooleanField(default=False)
    smart_rank_score = models.FloatField(default=0.0)

    # Placement & Flags
    featured_offer = models.BooleanField(default=False)
    custom_cta_label = models.CharField(max_length=100, blank=True, null=True)
    show_in_sections = models.BooleanField(default=True)
    link_to_contest = models.URLField(blank=True, null=True)
    vendor_visibility = models.BooleanField(default=True)
    platform_type = models.CharField(max_length=50, blank=True, null=True)
    product_position_rank = models.IntegerField(default=0)
    sponsored_flag = models.BooleanField(default=False)
    fraud_flag = models.BooleanField(default=False)

    # Targeting & Behavior
    success_ratio_req = models.FloatField(default=0.0)
    geo_targeting = models.TextField(blank=True, null=True)
    user_targeting_tags = models.TextField(blank=True, null=True)
    click_behavior = models.TextField(blank=True, null=True)
    offer_wall = models.BooleanField(default=False)
    trigger_badge_unlock = models.BooleanField(default=False)

    # Pricing & Purchase Rules
    min_cart_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    product_inr_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    product_quebes_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    enable_max_user = models.BooleanField(default=False)
    max_purchase_per_user = models.IntegerField(default=1)

    # Inventory & Delivery
    inventory = models.IntegerField(default=0)
    credited_at = models.DateTimeField(auto_now_add=True)
    tiered_delivery = models.BooleanField(default=False)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    product_actual_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    net_quantity = models.CharField(max_length=100, blank=True, null=True)

    # Product Details
    how_to_use = models.TextField(blank=True, null=True)
    ingredients = models.TextField(blank=True, null=True)
    key_benefits = models.TextField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    trust_badge = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.product_name


# Carousel Images
class TrialProductCarousel(models.Model):
    product = models.ForeignKey(TrialProduct, on_delete=models.CASCADE, related_name="carousel_images")
    image = models.ImageField(upload_to="trialstore/carousel/")

    def __str__(self):
        return f"Carousel for {self.product.product_name}"


# Milestone
class TrialProductMilestone(models.Model):
    product = models.ForeignKey(TrialProduct, on_delete=models.CASCADE, related_name="milestones")
    milestone_name = models.CharField(max_length=255)
    milestone_type = models.CharField(max_length=100)
    milestone_description = models.TextField(blank=True, null=True)
    milestone_payout = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    feedback_required = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.milestone_name} - {self.product.product_name}"


# Ads (for monetisation inside Trial Store)
class TrialStoreAd(models.Model):
    ad_name = models.CharField(max_length=255)
    ad_banner = models.ImageField(upload_to="trialstore/ads/", blank=True, null=True)
    ad_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.ad_name


# Feedback
class TrialStoreFeedback(models.Model):
    product = models.ForeignKey(TrialProduct, on_delete=models.CASCADE, related_name="feedbacks")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review_text = models.TextField(blank=True, null=True)
    rating = models.IntegerField(default=0)  # 1 to 5 stars
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for {self.product.product_name} by {self.user.username}"

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TrialAd(models.Model):
    AD_TYPE_CHOICES = [
        ('CPM', 'Cost Per Mille (1000 impressions)'),
        ('CPC', 'Cost Per Click'),
    ]

    ad_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    advertiser = models.CharField(max_length=255, blank=True, null=True)
    ad_type = models.CharField(max_length=10, choices=AD_TYPE_CHOICES, default='CPM')
    cpm_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # ₹ per 1000 impressions
    cpc_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # ₹ per click
    frequency_cap = models.IntegerField(default=3, help_text="Max impressions per user for this ad")
    boost_percentage = models.PositiveIntegerField(default=0, help_text="Increase cost by % (30,40,etc.)")
    target_geo = models.CharField(max_length=255, blank=True, null=True)
    target_tags = models.TextField(blank=True, null=True, help_text="Comma separated targeting tags")
    platform_type = models.CharField(max_length=50, default="All")

    banner_image = models.ImageField(upload_to="ads/banner/", blank=True, null=True)
    video_file = models.FileField(upload_to="ads/video/", blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def effective_cpm(self):
        """Apply boost percentage if any"""
        return self.cpm_rate + (self.cpm_rate * self.boost_percentage / 100)

    def effective_cpc(self):
        """Apply boost percentage if any"""
        return self.cpc_rate + (self.cpc_rate * self.boost_percentage / 100)

    def __str__(self):
        return f"{self.title} ({self.ad_type})"


class AdImpression(models.Model):
    ad = models.ForeignKey(TrialAd, on_delete=models.CASCADE, related_name="impressions")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    last_seen = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} saw {self.ad} {self.count} times"


class AdClick(models.Model):
    ad = models.ForeignKey(TrialAd, on_delete=models.CASCADE, related_name="clicks")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} clicked {self.ad}"
