from django.urls import path
from .views import (
    BrandStoreCreateAPIView,
    BrandStoreListAPIView,
    BrandStoreDetailAPIView,
    BrandStorePostbackView,
)

urlpatterns = [
    # CRUD Endpoints
    path('brand-stores/', BrandStoreListAPIView.as_view(), name='brandstore-list'),          # GET all brandstores
    path('brand-stores/create/', BrandStoreCreateAPIView.as_view(), name='brandstore-create'),  # POST new brandstore
    path('brand-stores/<int:id>/', BrandStoreDetailAPIView.as_view(), name='brandstore-detail'), # GET/PUT/PATCH/DELETE by id

    # Postback Endpoint
    path('brand-stores/postback/', BrandStorePostbackView.as_view(), name='brandstore-postback'),
]
