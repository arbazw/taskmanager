from django.contrib.auth.models import User
from rest_framework import generics, permissions
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from .permissions import IsOwnerOrAdmin

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Task.objects.all()
        completed = self.request.query_params.get("completed")
        if completed is not None:
            if completed.lower() == "true":
                queryset = queryset.filter(completed=True)
            if completed.lower() == "false":
                queryset = queryset.filter(completed=False)
        user = self.request.user
        if user.is_authenticated and not user.is_staff:
            queryset = queryset.filter(owner=user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]
