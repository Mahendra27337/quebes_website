import django_filters
from .models import UserProfile

class UserProfileFilter(django_filters.FilterSet):
    class Meta:
        model = UserProfile
        fields = {
            "gender": ["exact"],
            "city": ["exact", "icontains"],
            "state": ["exact"],
            "profession": ["exact", "icontains"],
            "industry": ["exact"],
            "annual_income": ["gte", "lte"],
            "credit_score": ["gte", "lte"],
            "open_to_travel": ["exact"],
            "smoking_habit": ["exact"],
            "alcohol_use": ["exact"],
            "diet": ["exact"],
        }
