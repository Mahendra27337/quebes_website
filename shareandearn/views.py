from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import ShareAndEarnOffer, ShareAndEarnMilestone, Referral
from .serializers import ShareAndEarnOfferSerializer, ShareAndEarnMilestoneSerializer, ReferralSerializer


class ShareAndEarnOfferViewSet(viewsets.ModelViewSet):
    queryset = ShareAndEarnOffer.objects.all()
    serializer_class = ShareAndEarnOfferSerializer

    @action(detail=True, methods=["post"])
    def add_referral(self, request, pk=None):
        """ Add referral (supports MLM by auto-increasing level) """
        offer = self.get_object()
        referrer_id = request.data.get("referrer_id")
        referee_id = request.data.get("referee_id")

        if not referrer_id or not referee_id:
            return Response({"error": "referrer_id and referee_id required"}, status=status.HTTP_400_BAD_REQUEST)

        # Level 1 referral
        referral = Referral.objects.create(offer=offer, referrer_id=referrer_id, referee_id=referee_id, level=1)

        # MLM cascade (if referee refers further, increase level)
        parent_referrals = Referral.objects.filter(offer=offer, referee_id=referrer_id)
        for parent in parent_referrals:
            Referral.objects.create(
                offer=offer,
                referrer_id=parent.referrer_id,
                referee_id=referee_id,
                level=parent.level + 1
            )

        return Response(ReferralSerializer(referral).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def check_fraud(self, request, pk=None):
        """ Simple fraud detection rule """
        offer = self.get_object()
        total_referrals = offer.referrals.count()
        total_milestones = offer.milestones.count()

        if total_referrals > 50 and total_milestones == 0:
            offer.fraud_flag = True
        else:
            offer.fraud_flag = False
        offer.save()

        return Response({"fraud_flag": offer.fraud_flag}, status=status.HTTP_200_OK)


class ShareAndEarnMilestoneViewSet(viewsets.ModelViewSet):
    queryset = ShareAndEarnMilestone.objects.all()
    serializer_class = ShareAndEarnMilestoneSerializer


class ReferralViewSet(viewsets.ModelViewSet):
    queryset = Referral.objects.all()
    serializer_class = ReferralSerializer
