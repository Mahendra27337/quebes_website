from django.urls import path
from .task_views import TaskCreateAPIView, TaskListAPIView

urlpatterns = [
    path('tasks/create/', TaskCreateAPIView.as_view(), name='task-create'),
    path('tasks/', TaskListAPIView.as_view(), name='task-list'),
]
