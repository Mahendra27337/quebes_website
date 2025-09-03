from django.contrib import admin
from .models import UserProfile, ReferralIncome, Vendor, Company, MilestoneType, Milestone, Task

admin.site.register(UserProfile)
admin.site.register(ReferralIncome)
admin.site.register(Vendor)
admin.site.register(Company)
admin.site.register(MilestoneType)
admin.site.register(Milestone)
admin.site.register(Task)

from django.contrib import admin
from .models import Contest, Banner

admin.site.register(Contest)
admin.site.register(Banner)

