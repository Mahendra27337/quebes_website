from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from trialstore.views import (
    TrialVendorViewSet, TrialProductViewSet, TrialProductCarouselViewSet,
    TrialProductMilestoneViewSet, TrialStoreAdViewSet, TrialStoreFeedbackViewSet
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ques3.urls')),
    path('api/brandstore/', include('brandstore.urls')),
    path("digitalstore/", include("digitalstore.urls")),
    path("api/trialstore/", include("trialstore.urls")),
    path('api/milestones/', include('milestones.urls')),
    path("api/walk/", include("walkandearn.urls")),
    path("api/mlm/", include("mlm.urls")),
    path('api/religiousstore/', include('religiousstore.urls')),
    path("api/scratchcards/", include("scratchcards.urls")),
    path("api/spinwheel/", include("spinwheel.urls")),
    path("api/", include("performandearn.urls")),
    path("performandearn/", include("performandearn.urls")),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)














