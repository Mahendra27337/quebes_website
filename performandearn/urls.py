from django.urls import path
from . import views

urlpatterns = [
    # 🔹 Perform & Earn (Offer CRUD)
    path("perform/", views.PerformAndEarnListCreateView.as_view(), name="perform-list-create"),
    path("perform/<int:pk>/", views.PerformAndEarnDetailView.as_view(), name="perform-detail"),

    # 🔹 User tasks (progress on offers)
    path("user-task/", views.UserPerformTaskCreateView.as_view(), name="user-task-create"),
    path("user-task/<int:pk>/complete/", views.UserPerformTaskCompleteView.as_view(), name="user-task-complete"),

    # 🔹 Vendor milestone callback
    path("milestone/callback/", views.milestone_callback, name="milestone-callback"),

    # 🔹 Get full task detail + milestone progress
    path("task/<int:task_id>/", views.perform_task_detail, name="perform-task-detail"),
]


