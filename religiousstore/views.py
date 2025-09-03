from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import ReligiousStore
from .serializers import ReligiousStoreSerializer

class ReligiousStoreViewSet(viewsets.ModelViewSet):
    queryset = ReligiousStore.objects.all()
    serializer_class = ReligiousStoreSerializer
    permission_classes = [permissions.IsAuthenticated]
