from rest_framework import serializers
from .models import DigitalProduct, DigitalPurchase


class DigitalProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalProduct
        fields = "__all__"


class DigitalPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalPurchase
        fields = "__all__"
