from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .task_models import Task
from .task_serializers import TaskSerializer

class TaskCreateAPIView(APIView):
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response({'message': 'Task created', 'task_id': task.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskListAPIView(APIView):
    def get(self, request):
        section = request.query_params.get('section')
        queryset = Task.objects.all()
        if section:
            queryset = queryset.filter(section=section)
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)
