from django.contrib import admin
from datetime import date
from .models import (
    UserProfile, ReferralIncome, Vendor, Company,
    MilestoneType, Milestone, Task, Contest, Banner
)


# --------------------------
# Custom Filters
# --------------------------
class AgeRangeFilter(admin.SimpleListFilter):
    title = "Age Range"
    parameter_name = "age_range"

    def lookups(self, request, model_admin):
        return [
            ("<20", "Below 20"),
            ("20-30", "20-30"),
            ("30-40", "30-40"),
            ("40-50", "40-50"),
            ("50+", "50 and above"),
        ]

    def queryset(self, request, queryset):
        today = date.today()
        if self.value():
            if self.value() == "<20":
                cutoff = today.replace(year=today.year - 20)
                return queryset.filter(dob__gt=cutoff)
            elif self.value() == "20-30":
                return queryset.filter(dob__lte=today.replace(year=today.year - 20),
                                       dob__gt=today.replace(year=today.year - 30))
            elif self.value() == "30-40":
                return queryset.filter(dob__lte=today.replace(year=today.year - 30),
                                       dob__gt=today.replace(year=today.year - 40))
            elif self.value() == "40-50":
                return queryset.filter(dob__lte=today.replace(year=today.year - 40),
                                       dob__gt=today.replace(year=today.year - 50))
            elif self.value() == "50+":
                return queryset.filter(dob__lte=today.replace(year=today.year - 50))
        return queryset


class IncomeRangeFilter(admin.SimpleListFilter):
    title = "Annual Income"
    parameter_name = "income_range"

    def lookups(self, request, model_admin):
        return [
            ("<5L", "Below 5 Lakhs"),
            ("5-10L", "5-10 Lakhs"),
            ("10-20L", "10-20 Lakhs"),
            ("20L+", "20 Lakhs and above"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "<5L":
            return queryset.filter(annual_income__lt=500000)
        elif self.value() == "5-10L":
            return queryset.filter(annual_income__gte=500000, annual_income__lt=1000000)
        elif self.value() == "10-20L":
            return queryset.filter(annual_income__gte=1000000, annual_income__lt=2000000)
        elif self.value() == "20L+":
            return queryset.filter(annual_income__gte=2000000)
        return queryset


class CreditScoreFilter(admin.SimpleListFilter):
    title = "Credit Score"
    parameter_name = "credit_score_range"

    def lookups(self, request, model_admin):
        return [
            ("<600", "Poor (<600)"),
            ("600-700", "Fair (600-700)"),
            ("700-750", "Good (700-750)"),
            ("750+", "Excellent (750+)"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "<600":
            return queryset.filter(credit_score__lt=600)
        elif self.value() == "600-700":
            return queryset.filter(credit_score__gte=600, credit_score__lt=700)
        elif self.value() == "700-750":
            return queryset.filter(credit_score__gte=700, credit_score__lt=750)
        elif self.value() == "750+":
            return queryset.filter(credit_score__gte=750)
        return queryset


# --------------------------
# Register other models
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
# Custom UserProfile admin
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
        "gender", "city", "state", "profession", "industry",
        "work_status", "highest_qualification",
        "primary_language", "secondary_language",
        "open_to_travel", "vehicle_type",
        "smoking_habit", "alcohol_use", "diet",
        AgeRangeFilter,        # ✅ Age filter
        IncomeRangeFilter,     # ✅ Income filter
        CreditScoreFilter,     # ✅ Credit Score filter
    )
    readonly_fields = ("user", "email")

    fieldsets = (
        ("Personal Info", {
            "fields": ("user", "name", "gender", "dob", "contact_number", "email",
                       "blood_group", "emergency_contact", "address", "area", "pin",
                       "city", "state", "profile_photo")
        }),
        ("Professional", {
            "fields": ("work_status", "profession", "experience_years", "annual_income",
                       "company", "industry")
        }),
        ("Education", {
            "fields": ("highest_qualification", "institute_name", "education_type", "board_university")
        }),
        ("Bank & Cards", {
            "fields": ("bank_name", "card_type", "upi_id", "credit_score")
        }),
        ("Family", {
            "fields": ("family_members",)
        }),
        ("Languages", {
            "fields": ("primary_language", "secondary_language", "proficiency_level")
        }),
        ("Travel & Accessibility", {
            "fields": ("open_to_travel", "vehicle_type", "vehicle_brand", "purchase_year")
        }),
        ("Lifestyle", {
            "fields": ("smoking_habit", "alcohol_use", "physical_activity", "diet")
        }),
        ("Medical", {
            "fields": ("illness", "medications")
        }),
    )


    # ----------------------
    # Bulk Admin Actions
    # ----------------------
    actions = ["assign_task", "assign_contest", "mark_as_targeted"]

    def assign_task(self, request, queryset):
        """Bulk assign a default Task to selected users"""
        task = Task.objects.first()  # TODO: Replace with selection logic
        for profile in queryset:
            # link task to profile if you have a UserTask model
            print(f"Assigned {task} to {profile.user}")
        self.message_user(request, f"{queryset.count()} users assigned to task {task}.")

    assign_task.short_description = "Assign Task to selected users"

    def assign_contest(self, request, queryset):
        """Bulk assign a default Contest to selected users"""
        contest = Contest.objects.first()
        for profile in queryset:
            print(f"Assigned {contest} to {profile.user}")
        self.message_user(request, f"{queryset.count()} users assigned to contest {contest}.")

    assign_contest.short_description = "Assign Contest to selected users"

    def mark_as_targeted(self, request, queryset):
        """Mark selected users as targeted"""
        queryset.update(open_to_travel=True)  # Example flag
        self.message_user(request, f"{queryset.count()} users marked as targeted.")

    mark_as_targeted.short_description = "Mark selected users as targeted"
