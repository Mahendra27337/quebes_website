from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone


class ShareAndEarnOffer(models.Model):
    # Basic identifiers
    yes_id = models.CharField(max_length=50, unique=True)
    offer_name_se = models.CharField(max_length=255)
    vendor_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)

    # Branding
    offer_brand_info_se = models.TextField()
    offer_brand_benefits_se = models.TextField(blank=True, null=True)

    # Media
    offer_logo_se = models.ImageField(upload_to="shareandearn/logos/")
    offer_banner_image_se = models.ImageField(upload_to="shareandearn/banners/")
    se_offer_video_file = models.FileField(upload_to="shareandearn/videos/", blank=True, null=True)
    se_offer_video_youtube = models.URLField(blank=True, null=True)

    # Offer details
    terms_conditions_se = models.TextField()
    how_to_earn_se = models.TextField(blank=True, null=True)
    whom_to_sell_se = models.TextField(blank=True, null=True)

    # Payouts
    task_payout_amount_se = models.DecimalField(max_digits=10, decimal_places=2)
    referral_payout_se = models.DecimalField(max_digits=10, decimal_places=2)

    # Tracking
    se_offer_link = models.URLField()
    share_and_earn_enabled = models.BooleanField(default=True)
    travel_required = models.BooleanField(default=False)

    # Categorization
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100, blank=True, null=True)

    daily_task = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()
    credit_type = models.CharField(max_length=50)
    tracking_type = models.CharField(max_length=50)
    payout_time_info = models.CharField(max_length=100)
    task_of_the_day = models.BooleanField(default=False)

    confirmation_time_hours = models.PositiveIntegerField(default=24)
    available_for_level1 = models.BooleanField(default=True)
    featured_partner = models.BooleanField(default=False)

    se_custom_cta_label = models.CharField(max_length=100, blank=True, null=True)
    se_no_of_people_availed = models.PositiveIntegerField(default=0)

    se_smart_rank_score_filter = models.CharField(max_length=50, blank=True, null=True)
    se_smart_rank_score = models.FloatField(default=0.0)

    show_in_sections = models.BooleanField(default=True)
    link_to_contest = models.URLField(blank=True, null=True)
    vendor_visibility = models.BooleanField(default=True)
    platform_type = models.CharField(max_length=50)

    se_task_tag = models.JSONField(default=list)  # store multiple tags
    task_position_rank = models.PositiveIntegerField(default=0)

    sponsored_flag = models.BooleanField(default=False)
    fraud_flag = models.BooleanField(default=False)
    success_ratio_req = models.FloatField(default=0.5)


    click_behavior = models.CharField(max_length=50, default="default")
    offer_wall = models.BooleanField(default=False)

    # Review flags
    trigger_badge_unlock = models.BooleanField(default=False)
    review_for_task_required = models.BooleanField(default=False)
    review_module_for_task = models.CharField(max_length=255, blank=True, null=True)
    my_lead = models.BooleanField(default=False)
    website_task_review_module_se = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.offer_name_se


class ShareAndEarnMilestone(models.Model):
    offer = models.ForeignKey(ShareAndEarnOffer, related_name="milestones", on_delete=models.CASCADE)
    milestone_name = models.CharField(max_length=255)
    milestone_type = models.CharField(max_length=50)
    milestone_description = models.TextField()
    milestone_payout = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.offer.offer_name_se} - {self.milestone_name}"


class Referral(models.Model):
    offer = models.ForeignKey(ShareAndEarnOffer, related_name="referrals", on_delete=models.CASCADE)
    referrer_id = models.CharField(max_length=100)  # user who shared
    referee_id = models.CharField(max_length=100)   # user who joined/clicked
    level = models.PositiveIntegerField(default=1)  # MLM: Level 1, 2, 3...
    created_at = models.DateTimeField(default=timezone.now)

    # To allow same referee to join via different referrers
    class Meta:
        unique_together = ("offer", "referrer_id", "referee_id", "level")

    def __str__(self):
        return f"{self.referrer_id} → {self.referee_id} (Level {self.level})"

