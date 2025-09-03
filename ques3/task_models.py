from django.db import models

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Company(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Milestone(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    description = models.TextField()
    payout = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return self.name

class Task(models.Model):
    SECTION_CHOICES = (
        ('share', 'Share and Earn'),
        ('perform', 'Perform and Earn'),
    )
    section = models.CharField(max_length=10, choices=SECTION_CHOICES)
    offer_name = models.CharField(max_length=255)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
    brand_info = models.TextField()
    brand_benefits = models.TextField()
    milestones = models.ManyToManyField(Milestone, blank=True)
    terms_conditions = models.TextField()
    how_to_earn = models.TextField()
    whom_to_sell = models.TextField(blank=True, null=True)
    offer_logo = models.ImageField(upload_to='offers/logos/')
    offer_banner = models.ImageField(upload_to='offers/banners/')
    offer_video_file = models.FileField(upload_to='offers/videos/', null=True, blank=True)
    offer_video_youtube = models.URLField(null=True, blank=True)
    task_payout = models.DecimalField(max_digits=10, decimal_places=2)
    referral_payout = models.DecimalField(max_digits=10, decimal_places=2)
    offer_link = models.URLField()
    travel_required = models.BooleanField(null=True, blank=True)
    category = models.CharField(max_length=255)
    sub_category = models.BooleanField(default=False)
    daily_task = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
    credit_type = models.CharField(max_length=255, blank=True, null=True)
    tracking_type = models.BooleanField(default=False)
    payout_time = models.CharField(max_length=255)
    task_of_the_day = models.BooleanField(default=False)
    confirmation_time = models.CharField(max_length=100)
    available_for_level_1 = models.BooleanField(default=False)
    featured_partner = models.BooleanField(default=False)
    custom_cta_label = models.CharField(max_length=255)
    smart_rank_score_filter = models.BooleanField(default=False)
    smart_rank_score = models.IntegerField()
    show_in_sections = models.CharField(max_length=255)
    link_to_contest = models.URLField(null=True, blank=True)
    vendor_visibility = models.CharField(max_length=255)
    platform_type = models.CharField(max_length=255)
    task_position_rank = models.IntegerField()
    sponsored_flag = models.BooleanField(default=False)
    fraud_flag = models.BooleanField(default=False)
    success_ratio_req = models.BooleanField(default=False)
    geo_targeting = models.CharField(max_length=255)
    user_targeting_tags = models.CharField(max_length=255)
    click_behavior = models.CharField(max_length=255)
    offer_wall = models.BooleanField(default=False)
    trigger_badge_unlock = models.BooleanField(default=False)
    review_module = models.BooleanField(default=False)
    my_lead = models.BooleanField(default=False)
    website_review_module = models.BooleanField(default=False)
    show_in_perform_if_share_enabled = models.BooleanField(default=False)
