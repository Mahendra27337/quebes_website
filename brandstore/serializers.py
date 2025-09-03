from rest_framework import serializers
from .models import BrandStore, BrandStoreMilestone


class BrandStoreMilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandStoreMilestone
        fields = "__all__"
        extra_kwargs = {"brand_store": {"read_only": True}}  # prevent user from overriding


class BrandStoreSerializer(serializers.ModelSerializer):
    milestones = BrandStoreMilestoneSerializer(many=True, required=False)

    class Meta:
        model = BrandStore
        fields = "__all__"

    def create(self, validated_data):
        milestones_data = validated_data.pop("milestones", [])
        brand_store = BrandStore.objects.create(**validated_data)

        # create nested milestones
        for milestone in milestones_data:
            BrandStoreMilestone.objects.create(brand_store=brand_store, **milestone)

        return brand_store

    def update(self, instance, validated_data):
        milestones_data = validated_data.pop("milestones", [])

        # update BrandStore fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Replace existing milestones with new ones
        if milestones_data:
            instance.milestones.all().delete()
            for milestone in milestones_data:
                BrandStoreMilestone.objects.create(brand_store=instance, **milestone)

        return instance

    def validate(self, data):
        # Fraud prevention check
        if data.get('success_ratio_req') and data['success_ratio_req'] > 1:
            raise serializers.ValidationError("Success ratio requirement cannot exceed 1.0 (100%).")

        # Date validation
        if data.get('start_date') and data.get('end_date'):
            if data['end_date'] < data['start_date']:
                raise serializers.ValidationError("End date cannot be earlier than start date.")

        return data

