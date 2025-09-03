from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import DigitalProduct, DigitalPurchase, DigitalProductMilestone
from .serializers import (
    DigitalProductSerializer,
    DigitalPurchaseSerializer,
    DigitalProductMilestoneSerializer
)
import requests


class DigitalProductViewSet(viewsets.ModelViewSet):
    queryset = DigitalProduct.objects.all()
    serializer_class = DigitalProductSerializer

    # 🔹 Add milestone to a product
    @action(detail=True, methods=["post"])
    def add_milestone(self, request, pk=None):
        product = self.get_object()
        serializer = DigitalProductMilestoneSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(digital_product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 🔹 List milestones of a product
    @action(detail=True, methods=["get"])
    def milestones(self, request, pk=None):
        product = self.get_object()
        milestones = product.milestones.all()
        serializer = DigitalProductMilestoneSerializer(milestones, many=True)
        return Response(serializer.data)

    # 🔹 Delete a milestone from a product
    @action(detail=True, methods=["delete"], url_path="milestones/(?P<milestone_id>[^/.]+)")
    def delete_milestone(self, request, pk=None, milestone_id=None):
        product = self.get_object()
        milestone = get_object_or_404(DigitalProductMilestone, pk=milestone_id, digital_product=product)
        milestone.delete()
        return Response({"status": "Milestone deleted"}, status=status.HTTP_204_NO_CONTENT)


class DigitalPurchaseViewSet(viewsets.ModelViewSet):
    queryset = DigitalPurchase.objects.all()
    serializer_class = DigitalPurchaseSerializer

    @action(detail=True, methods=["post"])
    def mark_completed(self, request, pk=None):
        purchase = get_object_or_404(DigitalPurchase, pk=pk)
        purchase.status = "completed"
        purchase.save()

        # Trigger postback if URL exists
        if purchase.postback_url:
            try:
                requests.post(purchase.postback_url, data={
                    "purchase_id": purchase.id,
                    "product_id": purchase.product.id,
                    "user_id": purchase.user_id,
                    "android_id": purchase.android_id,
                    "imei_number": purchase.imei_number,
                    "status": "completed"
                })
            except Exception as e:
                print(f"Postback failed: {e}")

        # Trigger callback if URL exists
        if purchase.callback_url:
            try:
                requests.post(purchase.callback_url, data={
                    "purchase_id": purchase.id,
                    "status": "completed"
                })
            except Exception as e:
                print(f"Callback failed: {e}")

        return Response({"status": "Purchase marked as completed"}, status=status.HTTP_200_OK)

