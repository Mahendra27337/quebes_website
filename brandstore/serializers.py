from rest_framework import serializers
from .models import BrandStore

class BrandStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandStore
        fields = '__all__'  # include all model fields

    def validate(self, data):
        # Example fraud prevention check
        if data.get('success_ratio_req') and data['success_ratio_req'] > 1:
            raise serializers.ValidationError("Success ratio requirement cannot exceed 1.0 (100%).")
        
        # Date validation
        if data.get('start_date') and data.get('end_date'):
            if data['end_date'] < data['start_date']:
                raise serializers.ValidationError("End date cannot be earlier than start date.")
        
        return data
