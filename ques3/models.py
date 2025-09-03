from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid




# Extended User Profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Personal Info
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=20)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField()
    dob = models.DateField()
    blood_group = models.CharField(max_length=5)
    emergency_contact = models.CharField(max_length=20)
    address = models.TextField()
    area = models.CharField(max_length=100)
    pin = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)

    # Professional
    work_status = models.CharField(max_length=50)
    profession = models.CharField(max_length=100)
    experience_years = models.IntegerField()
    annual_income = models.FloatField()
    company = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)

    # Education
    highest_qualification = models.CharField(max_length=100)
    institute_name = models.CharField(max_length=255)
    education_type = models.CharField(max_length=100)
    board_university = models.CharField(max_length=255)

    # Bank & Cards
    bank_name = models.CharField(max_length=100)
    card_type = models.CharField(max_length=100)
    upi_id = models.CharField(max_length=100, blank=True, null=True)
    credit_score = models.IntegerField(blank=True, null=True)

    # Family
    family_members = models.JSONField(default=list)  # [{"relation": "", "age_group": "", "dependent": true}]

    # Languages
    primary_language = models.CharField(max_length=100)
    secondary_language = models.CharField(max_length=100)
    proficiency_level = models.CharField(max_length=100)

    # Travel & Accessibility
    open_to_travel = models.BooleanField(default=False)
    vehicle_type = models.CharField(max_length=100)
    vehicle_brand = models.CharField(max_length=100)
    purchase_year = models.IntegerField()

    # Lifestyle
    smoking_habit = models.CharField(max_length=100)
    alcohol_use = models.CharField(max_length=100)
    physical_activity = models.CharField(max_length=100)
    diet = models.CharField(max_length=100)

    # Medical
    illness = models.TextField(blank=True, null=True)
    medications = models.TextField(blank=True, null=True)

    # Referrals
referral_by = models.ForeignKey(User, null=True, blank=True, related_name='referrals', on_delete=models.SET_NULL)
referral_code = models.CharField(max_length=12, unique=True, blank=True)  # New field

    # Resume/Skills skills = models.TextField(blank=True, null=True)
resume = models.FileField(upload_to='resumes/', blank=True, null=True)

smart_rank_score = models.IntegerField(default=0)

def __str__(self):
        return self.user.username

def save(self, *args, **kwargs):
 if not self.referral_code:  
            # Generate unique referral code
            self.referral_code = str(uuid.uuid4().hex[:8].upper())
 super().save(*args, **kwargs)
    
# MLM Referral History
class ReferralIncome(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='earned_referrals')
    referred_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral_source')
    level = models.IntegerField()
    income = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

# Admin-defined dropdowns
class Vendor(models.Model):
    name = models.CharField(max_length=100)

class Company(models.Model):
    name = models.CharField(max_length=100)

class MilestoneType(models.Model):
    name = models.CharField(max_length=100)

class Milestone(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(MilestoneType, on_delete=models.CASCADE)
    description = models.TextField()
    payout = models.FloatField()

# Task model
class Task(models.Model):
    SECTION_CHOICES = (("share", "Share & Earn"), ("perform", "Perform & Earn"))

    section = models.CharField(max_length=10, choices=SECTION_CHOICES)
offer_title = models.CharField(max_length=255)
vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True)
offer_brand_info = models.TextField()
offer_brand_benefits = models.TextField()
milestones = models.ManyToManyField(Milestone)
terms_conditions = models.TextField()
how_to_earn = models.TextField()
whom_to_sell = models.TextField(blank=True, null=True)
offer_logo = models.ImageField(upload_to='offers/')
offer_banner = models.ImageField(upload_to='offers/')
offer_video_file = models.FileField(upload_to='offers/videos/', blank=True, null=True)
offer_video_youtube = models.URLField(blank=True, null=True)
task_payout = models.FloatField()
referral_payout = models.FloatField()
offer_link = models.URLField()
travel_required = models.BooleanField(default=False)
category = models.CharField(max_length=100)
sub_category = models.CharField(max_length=100)
daily_task = models.BooleanField(default=False)
start_date = models.DateField()
end_date = models.DateField()
credit_type = models.CharField(max_length=100, blank=True, null=True)
tracking_type = models.BooleanField(default=False)
payout_time_info = models.TextField()
task_of_the_day = models.BooleanField(default=False)
confirmation_time = models.IntegerField()
available_for_level1 = models.BooleanField(default=False)
featured_partner = models.BooleanField(default=False)
custom_cta_label = models.CharField(max_length=100)
smart_rank_score = models.IntegerField()
show_in_sections = models.CharField(max_length=255)
link_to_contest = models.URLField(blank=True, null=True)
vendor_visibility = models.CharField(max_length=100)
platform_type = models.CharField(max_length=100)
task_position_rank = models.IntegerField()
sponsored_flag = models.BooleanField(default=False)
fraud_flag = models.BooleanField(default=False)
success_ratio_req = models.FloatField()
geo_targeting = models.JSONField(default=list)
user_targeting_tags = models.JSONField(default=list)
click_behavior = models.CharField(max_length=100)
offer_wall = models.BooleanField(default=False)
trigger_badge_unlock = models.BooleanField(default=False)
review_module_app = models.BooleanField(default=False)
my_lead = models.BooleanField(default=False)
website_task_review = models.BooleanField(default=False)
    
    
from django.db import models
from django.contrib.auth.models import User

class Contest(models.Model):
    REWARD_TYPE_CHOICES = [
        ('gift_card', 'Gift Card'),
        ('quebes', 'Quebes'),
        ('coupon', 'Coupon'),
        ('voucher', 'Voucher'),
        ('product', 'Product'),
    ]

    title = models.CharField(max_length=255)
    information = models.TextField()
    offer_type = models.CharField(max_length=100)
    offer_title = models.CharField(max_length=100)
    required_users = models.PositiveIntegerField()
    available_to_level1 = models.BooleanField(default=False)
    offer_eligibility_logic = models.TextField()
    user_tracking_logic = models.TextField()
    max_users = models.PositiveIntegerField()
    reward_type = models.CharField(max_length=50, choices=REWARD_TYPE_CHOICES)
    reward_payout = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gift_card_details = models.TextField(blank=True, null=True)
    coupon_details = models.TextField(blank=True, null=True)
    voucher_details = models.TextField(blank=True, null=True)
    product_details = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    banner = models.ImageField(upload_to='contest_banners/')
    video = models.FileField(upload_to='contest_videos/', null=True, blank=True)
    daily_limit = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class Banner(models.Model):
    TYPE_CHOICES = [
        ('banner', 'Banner'),
        ('video', 'Video')
    ]
    SCREEN_CHOICES = [
        ('home', 'Home Screen'),
        ('interstitial', 'Interstitial Offer Wall'),
        ('leaderboard_footer', 'Referral Leaderboard Footer'),
        ('subscription', 'Subscription Screen'),
        ('wallet_top', 'Wallet Top Bar')
    ]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='banners/', null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    screen = models.CharField(max_length=50, choices=SCREEN_CHOICES)
    placement_zone = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    link_url = models.URLField(null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    priority_ranking = models.IntegerField()
    time_of_day = models.TimeField(null=True, blank=True)
    banner_type = models.CharField(max_length=100)
    banner_tag = models.CharField(max_length=100)
    user_level = models.IntegerField()
    geo_targeting = models.TextField(null=True, blank=True)
    user_targeting_tags = models.TextField(null=True, blank=True)
    platform_type = models.CharField(max_length=100)
    vendor_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    ad_type = models.CharField(max_length=100, null=True, blank=True)
    ad_payout_type = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed')
    )
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reward_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)
updated_at = models.DateTimeField(auto_now=True)
    
class PostbackLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    payload = models.JSONField()
    received_at = models.DateTimeField(auto_now_add=True)

