from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from task.models import Task, Comment
from task.api.serializers import TaskSerializer, CommentSerializer
from project.models import Project


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only tasks from projects created by the current user"""
        return Task.objects.filter(project__created_by=self.request.user)

    def perform_create(self, serializer):
        project = serializer.validated_data.get('project')
        if project and project.created_by != self.request.user:
            raise PermissionError("Cannot add task to another user's project.")
        serializer.save()

    def perform_update(self, serializer):
        if serializer.instance.project.created_by != self.request.user:
            raise PermissionError("Cannot update task from another user's project.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.project.created_by != self.request.user:
            raise PermissionError("Cannot delete task from another user's project.")
        instance.delete()

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        task_pk = self.kwargs.get('task_pk')
        if task_pk:
            return Comment.objects.filter(
                task_id=task_pk,
                task__project__created_by=self.request.user
            ).select_related('author', 'task')
        return Comment.objects.none()

    def perform_create(self, serializer):
        task_pk = self.kwargs.get('task_pk')
        task = get_object_or_404(Task, pk=task_pk)
        
        # Permission check
        if task.project.created_by != self.request.user:
            raise PermissionError("You can only comment on tasks in your own projects.")

        serializer.save(author=self.request.user, task=task)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            self.perform_create(serializer)
            return Response({
                "message": "Comment added successfully!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        except PermissionError as e:
            return Response({"detail": str(e)}, status=status.HTTP_403_FORBIDDEN)