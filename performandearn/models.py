from django.db import models
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()


class PerformAndEarn(models.Model):
    id = models.AutoField(primary_key=True)
    offer_name = models.CharField(max_length=255)
    vendor_name = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)

    offer_brand_info = models.TextField()
    offer_brand_benefits = models.TextField(blank=True, null=True)

    # 🔑 allow multiple milestone sets
    milestone_sets = models.ManyToManyField(
        "milestones.MilestoneSet",
        blank=True,
        related_name="perform_offers"
    )

    terms_conditions = models.TextField()
    how_to_earn = models.TextField(blank=True, null=True)
    whom_to_sell = models.TextField(blank=True, null=True)

    offer_logo = models.ImageField(upload_to="performandearn/logo/")
    offer_banner = models.ImageField(upload_to="performandearn/banner/")

    offer_video_file = models.FileField(
        upload_to="performandearn/videos/", null=True, blank=True
    )
    offer_video_url = models.URLField(blank=True, null=True)

    task_payout_amount = models.DecimalField(max_digits=10, decimal_places=2)
    referral_payout = models.DecimalField(max_digits=10, decimal_places=2)

    pe_offer_link = models.URLField()
    share_and_earn_enabled = models.BooleanField(default=False)
    travel_required = models.BooleanField(default=False)

    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)

    daily_task = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()

    credit_type = models.CharField(max_length=50, blank=True, null=True)
    tracking_type = models.CharField(max_length=50, default="Postback")

    payout_time_info = models.CharField(max_length=255)
    task_of_day = models.BooleanField(default=False)
    confirmation_time = models.CharField(max_length=100, default="24h")

    available_for_level1 = models.BooleanField(default=True)
    featured_partner = models.BooleanField(default=False)

    pe_custom_cta_label = models.CharField(max_length=100, blank=True, null=True)
    pe_no_people_availed = models.CharField(max_length=100, blank=True, null=True)

    pe_smart_rank_score_filter = models.BooleanField(default=False)
    pe_smart_rank_score = models.IntegerField(default=0)

    show_in_sections = models.CharField(max_length=100, default="general")
    link_to_contest = models.BooleanField(default=False)
    vendor_visibility = models.BooleanField(default=True)

    platform_type = models.CharField(max_length=100, default="all")
    pe_task_tag = models.CharField(max_length=255, blank=True, null=True)

    task_position_rank = models.IntegerField(default=0)
    sponsored_flag = models.BooleanField(default=False)
    fraud_flag = models.BooleanField(default=False)
    success_ratio_required = models.BooleanField(default=False)

    geo_targeting = models.TextField(blank=True, null=True)
    user_targeting_tags = models.TextField(blank=True, null=True)

    click_behavior = models.CharField(max_length=50, default="redirect")
    offer_wall = models.BooleanField(default=False)

    trigger_badge_unlock = models.BooleanField(default=False)
    review_required = models.BooleanField(default=False)

    website_task_review_module = models.TextField(blank=True, null=True)
    my_lead = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.offer_name


class UserPerformTask(models.Model):
    """Tracks user participation in Perform & Earn"""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="perform_tasks")
    task = models.ForeignKey(PerformAndEarn, on_delete=models.CASCADE, related_name="user_tasks")

    status = models.CharField(
        max_length=20,
        choices=(("pending", "Pending"), ("completed", "Completed"), ("rejected", "Rejected")),
        default="pending",
    )
    reward_credited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def mark_completed(self):
        from mlm.utils import distribute_referral_income

        self.status = "completed"
        self.save()

        # distribute MLM referral income
        distribute_referral_income(self.user, Decimal(self.task.task_payout_amount))
