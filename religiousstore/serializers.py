from rest_framework import serializers
from .models import ReligiousStore

class ReligiousStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReligiousStore
        fields = "__all__"
