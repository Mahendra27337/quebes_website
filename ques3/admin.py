from django.contrib import admin
from .models import (
    UserProfile, ReferralIncome, Vendor, Company,
    MilestoneType, Milestone, Task, Contest, Banner
)


# --------------------------
# Register everything else
# --------------------------
admin.site.register(ReferralIncome)
admin.site.register(Vendor)
admin.site.register(Company)
admin.site.register(MilestoneType)
admin.site.register(Milestone)
admin.site.register(Task)
admin.site.register(Contest)
admin.site.register(Banner)


# --------------------------
# UserProfile with custom admin
# --------------------------
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user", "name", "gender", "city", "state",
        "profession", "annual_income", "credit_score"
    )
    search_fields = (
        "name", "city", "state", "profession",
        "company", "industry", "primary_language"
    )
    list_filter = (
        "gender",
        "city",
        "state",
        "profession",
        "industry",
        "work_status",
        "highest_qualification",
        "primary_language",
        "secondary_language",
        "open_to_travel",
        "vehicle_type",
        "smoking_habit",
        "alcohol_use",
        "diet",
    )
