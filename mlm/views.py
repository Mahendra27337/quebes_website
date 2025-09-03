from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import Referral, ReferralIncome
from .serializers import ReferralSerializer, ReferralIncomeSerializer
from .utils import distribute_referral_income
from decimal import Decimal


# API to create referral link / relation
class CreateReferralAPIView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        referred_by_id = request.data.get("referred_by_id")

        if not user_id or not referred_by_id:
            return Response({"error": "user_id and referred_by_id required"}, status=400)

        if user_id == referred_by_id:
            return Response({"error": "User cannot refer themselves"}, status=400)

        user = User.objects.get(id=user_id)
        referred_by = User.objects.get(id=referred_by_id)

        referral, created = Referral.objects.get_or_create(user=user)
        referral.referred_by = referred_by
        referral.save()

        return Response(ReferralSerializer(referral).data, status=201)


# API to trigger income distribution
class DistributeIncomeAPIView(APIView):
    def post(self, request):
        user_id = request.data.get("user_id")
        amount = request.data.get("amount")

        if not user_id or not amount:
            return Response({"error": "user_id and amount required"}, status=400)

        user = User.objects.get(id=user_id)
        distribute_referral_income(user, Decimal(amount))

        return Response({"message": "Income distributed successfully"})


# API to view incomes earned by a user
class UserIncomeListAPIView(generics.ListAPIView):
    serializer_class = ReferralIncomeSerializer

    def get_queryset(self):
        user_id = self.kwargs["user_id"]
        return ReferralIncome.objects.filter(user_id=user_id).order_by("-created_at")
