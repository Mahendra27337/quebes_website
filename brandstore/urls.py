from django.urls import path
from .views import BrandStorePostbackView

urlpatterns = [
    path('brand-store/postback/', BrandStorePostbackView.as_view(), name='brand-store-postback'),
]
