from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import MilestoneSet, Milestone, UserMilestone

class MilestoneInline(admin.TabularInline):
    model = Milestone
    extra = 0

@admin.register(MilestoneSet)
class MilestoneSetAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'content_type', 'object_id', 'created_at')
    search_fields = ('name',)
    inlines = [MilestoneInline]

@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'milestone_set', 'title', 'order', 'payout')
    list_filter = ('milestone_set',)
    ordering = ('milestone_set', 'order')

@admin.register(UserMilestone)
class UserMilestoneAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'milestone', 'status', 'submitted_at', 'reviewed_at')
    list_filter = ('status', 'milestone__milestone_set')
    search_fields = ('user__username', 'milestone__title', 'milestone__milestone_set__name')
    readonly_fields = ('submitted_at', 'reviewed_at')
