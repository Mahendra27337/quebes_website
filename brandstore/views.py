import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import BrandStore

class BrandStorePostbackView(APIView):
    def post(self, request):
        brand_store_id = request.data.get('brand_store_id')
        android_id = request.data.get('android_id')
        imei_number = request.data.get('imei_number')

        brand_store = get_object_or_404(BrandStore, pk=brand_store_id)
        brand_store.android_id = android_id
        brand_store.imei_number = imei_number

        # Fraud flag check example
        if brand_store.success_ratio_req > 0.5:  
            brand_store.fraud_flag = False
        else:
            brand_store.fraud_flag = True

        # Smart rank example
        if not brand_store.fraud_flag:
            brand_store.offer_position_rank += 1

        brand_store.save()

        # Callback to advertiser
        callback_url = f"https://advertiser.com/callback?offer_id={brand_store_id}&android_id={android_id}&imei={imei_number}"
        try:
            requests.get(callback_url, timeout=5)
        except Exception as e:
            print(f"Callback error: {e}")

        return Response({"status": "success", "message": "Postback recorded and callback sent"}, status=status.HTTP_200_OK)

