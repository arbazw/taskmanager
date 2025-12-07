from django.urls import path
from .views import RegisterView, TaskListCreateView, TaskRetrieveUpdateDestroyView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("tasks/", TaskListCreateView.as_view(), name="task-list-create"),
    path("tasks/<int:pk>/", TaskRetrieveUpdateDestroyView.as_view(), name="task-detail"),
]
