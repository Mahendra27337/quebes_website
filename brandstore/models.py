from django.db import models


class BrandStore(models.Model):
    brand_store_id = models.AutoField(primary_key=True)
    store_offer_name = models.CharField(max_length=255)
    vendor_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    offer_brand_info = models.TextField(blank=True, null=True)
    offer_brand_benefits = models.TextField(blank=True, null=True)

    # Tracking info
    android_id = models.CharField(max_length=255, blank=True, null=True)
    imei_number = models.CharField(max_length=255, blank=True, null=True)

    available_to_il1 = models.BooleanField(default=False)
    brand_store_terms_conditions = models.TextField(blank=True, null=True)
    whom_to_sell_how_it_works = models.TextField(blank=True, null=True)
    brand_store_offer_url = models.URLField(blank=True, null=True)
    credit_type = models.CharField(max_length=100, blank=True, null=True)
    tracking_type = models.CharField(max_length=100, blank=True, null=True)
    featured_offer = models.BooleanField(default=False)
    custom_cta_label = models.CharField(max_length=255, blank=True, null=True)
    show_in_sections = models.CharField(max_length=255, blank=True, null=True)
    link_to_contest = models.URLField(blank=True, null=True)
    trigger_badge_unlock = models.BooleanField(default=False)

    brand_logo = models.ImageField(upload_to='brand_store/logos/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='brand_store/banners/', blank=True, null=True)
    offer_video_file = models.FileField(upload_to='brand_store/videos/', blank=True, null=True)
    offer_video_youtube = models.URLField(blank=True, null=True)
    brand_store_task_payout = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    brand_store_referral_payout = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    travel_required = models.BooleanField(default=False)
    brand_store_category = models.CharField(max_length=100, blank=True, null=True)
    brand_store_sub_category = models.CharField(max_length=100, blank=True, null=True)
    daily_task = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
    
    brand_store_payout_info = models.TextField(blank=True, null=True)
    task_of_the_day = models.BooleanField(default=False)
    conversion_window_days = models.IntegerField(default=0)
    
    platform_type = models.CharField(max_length=100, blank=True, null=True)
    offer_position_rank = models.IntegerField(default=0)
    sponsored_flag = models.BooleanField(default=False)
    fraud_flag = models.BooleanField(default=False)
    success_ratio_req = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    geo_targeting = models.TextField(blank=True, null=True)
    user_targeting_tags = models.TextField(blank=True, null=True)
    click_behavior = models.CharField(max_length=100, blank=True, null=True)
    offer_wall = models.BooleanField(default=False)
    review_module_for_app = models.BooleanField(default=False)
    my_lead = models.BooleanField(default=False)
    
    brand_store_offer_type = models.CharField(max_length=100, blank=True, null=True)
    minimum_cart_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    carousel_image_1 = models.ImageField(upload_to='brand_store/carousel/', blank=True, null=True)
    carousel_image_2 = models.ImageField(upload_to='brand_store/carousel/', blank=True, null=True)
    carousel_image_3 = models.ImageField(upload_to='brand_store/carousel/', blank=True, null=True)
    carousel_image_4 = models.ImageField(upload_to='brand_store/carousel/', blank=True, null=True)

    def __str__(self):
        return self.store_offer_name


class BrandStoreMilestone(models.Model):
    brand_store = models.ForeignKey(BrandStore, related_name="milestones", on_delete=models.CASCADE)
    milestone_name = models.CharField(max_length=255)
    milestone_type = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    payout = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.milestone_name} ({self.brand_store.store_offer_name})"
