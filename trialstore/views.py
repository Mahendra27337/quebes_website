from rest_framework import viewsets, permissions
from .models import (
    TrialVendor, TrialProduct, TrialProductCarousel,
    TrialProductMilestone, TrialStoreAd, TrialStoreFeedback
)
from .serializers import (
    TrialVendorSerializer, TrialProductSerializer, TrialProductCarouselSerializer,
    TrialProductMilestoneSerializer, TrialStoreAdSerializer, TrialStoreFeedbackSerializer
)
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import TrialAd, AdImpression, AdClick
from .serializers import TrialAdSerializer, AdImpressionSerializer, AdClickSerializer

class TrialVendorViewSet(viewsets.ModelViewSet):
    queryset = TrialVendor.objects.all()
    serializer_class = TrialVendorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TrialProductViewSet(viewsets.ModelViewSet):
    queryset = TrialProduct.objects.all()
    serializer_class = TrialProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TrialProductCarouselViewSet(viewsets.ModelViewSet):
    queryset = TrialProductCarousel.objects.all()
    serializer_class = TrialProductCarouselSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TrialProductMilestoneViewSet(viewsets.ModelViewSet):
    queryset = TrialProductMilestone.objects.all()
    serializer_class = TrialProductMilestoneSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TrialStoreAdViewSet(viewsets.ModelViewSet):
    queryset = TrialStoreAd.objects.all()
    serializer_class = TrialStoreAdSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TrialStoreFeedbackViewSet(viewsets.ModelViewSet):
    queryset = TrialStoreFeedback.objects.all()
    serializer_class = TrialStoreFeedbackSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
      

class TrialAdViewSet(viewsets.ModelViewSet):
    queryset = TrialAd.objects.filter(active=True)
    serializer_class = TrialAdSerializer

    @action(detail=True, methods=['post'])
    def impression(self, request, pk=None):
        """Record ad impression (view)"""
        ad = self.get_object()
        user = request.user

        impression, created = AdImpression.objects.get_or_create(ad=ad, user=user)
        if impression.count < ad.frequency_cap:
            impression.count += 1
            impression.save()
            return Response({"message": "Impression recorded", "count": impression.count})
        else:
            return Response({"message": "Frequency cap reached"}, status=400)

    @action(detail=True, methods=['post'])
    def click(self, request, pk=None):
        """Record ad click"""
        ad = self.get_object()
        user = request.user
        AdClick.objects.create(ad=ad, user=user)
        return Response({"message": "Click recorded"})



