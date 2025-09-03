from rest_framework import serializers
from .models import DigitalProduct, DigitalPurchase, DigitalProductMilestone


class DigitalProductMilestoneSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)  # allow existing milestone update

    class Meta:
        model = DigitalProductMilestone
        fields = ["id", "milestone_name", "milestone_type", "milestone_description", "milestone_payout"]


class DigitalProductSerializer(serializers.ModelSerializer):
    milestones = DigitalProductMilestoneSerializer(many=True, required=False)

    class Meta:
        model = DigitalProduct
        fields = "__all__"

    def create(self, validated_data):
        milestones_data = validated_data.pop("milestones", [])
        product = DigitalProduct.objects.create(**validated_data)

        for milestone_data in milestones_data:
            DigitalProductMilestone.objects.create(digital_product=product, **milestone_data)

        return product

    def update(self, instance, validated_data):
        milestones_data = validated_data.pop("milestones", [])

        # update DigitalProduct fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if milestones_data:
            existing_ids = [m.id for m in instance.milestones.all()]
            sent_ids = [m.get("id") for m in milestones_data if m.get("id")]

            # delete milestones that were not sent
            for milestone in instance.milestones.all():
                if milestone.id not in sent_ids:
                    milestone.delete()

            # update or create milestones
            for milestone_data in milestones_data:
                milestone_id = milestone_data.get("id", None)
                if milestone_id and milestone_id in existing_ids:
                    # update existing milestone
                    milestone = DigitalProductMilestone.objects.get(id=milestone_id, digital_product=instance)
                    for attr, value in milestone_data.items():
                        setattr(milestone, attr, value)
                    milestone.save()
                else:
                    # create new milestone
                    DigitalProductMilestone.objects.create(digital_product=instance, **milestone_data)

        return instance


class DigitalPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalPurchase
        fields = "__all__"


