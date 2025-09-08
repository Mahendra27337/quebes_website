from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import UserProfileSerializer, TaskSerializer
from django.contrib.auth.models import User
from .models import UserProfile, ReferralIncome
from .serializers import ReferralSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import UserProfile
from .serializers import UserProfileSerializer
from .filters import UserProfileFilter


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"message": "Login successful"})
        return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
class UserProfileViewSet(viewsets.ModelViewSet):
  queryset = UserProfile.objects.all()
serializer_class = UserProfileSerializer
filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
filterset_class = UserProfileFilter
search_fields = ["name", "city", "state", "profession", "industry", "primary_language"]
ordering_fields = ["annual_income", "credit_score", "experience_years"]
    
class ReferralView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = request.user.userprofile
        serializer = ReferralSerializer(profile)
        return Response(serializer.data)

class TaskAPIView(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.generics import CreateAPIView
from .models import Task
from .serializers import TaskSerializer

class TaskCreateAPIView(CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


from rest_framework.generics import ListAPIView

class TaskListAPIView(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ReferralIncome, UserProfile
from django.contrib.auth.models import User

class OfferCompleteAPIView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        referral_amount = float(request.data.get('referral_amount', 0))

        try:
            user = User.objects.get(id=user_id)
            profile = UserProfile.objects.get(user=user)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Add referral income for up to 3 levels
        referrer = profile.referred_by
        levels = [0.4, 0.3, 0.3]  # Level 1, 2, 3

        for level_percent in levels:
            if not referrer:
                break
            ReferralIncome.objects.create(
                user=referrer,
                referred_user=user,
                amount=referral_amount * level_percent
            )
            referrer = referrer.referred_by

        return Response({'message': 'Referral income distributed'}, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ReferralIncome
from .serializers import ReferralIncomeSerializer

class ReferralHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        referral_incomes = ReferralIncome.objects.filter(user=request.user)
        serializer = ReferralIncomeSerializer(referral_incomes, many=True)
        return Response(serializer.data)


from rest_framework import generics, permissions
from .models import Contest, Banner
from .serializers import ContestSerializer, BannerSerializer

class ContestCreateAPIView(generics.CreateAPIView):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admin can create

class ContestListAPIView(generics.ListAPIView):
    serializer_class = ContestSerializer

    def get_queryset(self):
        queryset = Contest.objects.all()
        level = self.request.query_params.get('level')
        if level == '1':
            queryset = queryset.filter(available_to_level1=True)

        # Filter active contests
        active = self.request.query_params.get('active')
        if active == 'true':
            from datetime import date
            today = date.today()
            queryset = queryset.filter(start_date__lte=today, end_date__gte=today)

        return queryset

class BannerCreateAPIView(generics.CreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [permissions.IsAdminUser]

class BannerListAPIView(generics.ListAPIView):
    serializer_class = BannerSerializer
    queryset = Banner.objects.all()

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny
from django.shortcuts import get_object_or_404
from .models import Task, PostbackLog
from .serializers import TaskSerializer
import requests

class TaskCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class TaskPostbackAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        task_id = request.data.get('task_id')
        payload = request.data
        task = get_object_or_404(Task, id=task_id)
        task.status = 'completed'
        task.save()
        self.credit_user(task)
        PostbackLog.objects.create(task=task, payload=payload)
        self.trigger_callback(task)
        return Response({"message": "Task completed and credited."})

    def credit_user(self, task):
        # Implement your wallet credit logic here
        pass

    def trigger_callback(self, task):
        callback_url = "https://vendor.example.com/callback"
        data = {"task_id": task.id, "status": task.status}
        try:
            requests.post(callback_url, json=data)
        except Exception:
            pass
