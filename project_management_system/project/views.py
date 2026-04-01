from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.db import models

from project.models import Project
from project.api.serializers import ProjectSerializer, ProjectListSerializer   # ← Correct this line

User = get_user_model()


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectListSerializer
        return ProjectSerializer

    def get_queryset(self):
        user = self.request.user
        return Project.objects.filter(
            models.Q(created_by=user) |
            models.Q(manager=user) |
            models.Q(members=user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def add_members(self, request, pk=None):
        project = self.get_object()

        if project.created_by != request.user and project.manager != request.user:
            return Response({"detail": "Only project creator or manager can add members."}, 
                            status=status.HTTP_403_FORBIDDEN)

        member_ids = request.data.get('member_ids', [])
        if not member_ids:
            return Response({"detail": "member_ids field is required"}, status=status.HTTP_400_BAD_REQUEST)

        users_to_add = User.objects.filter(id__in=member_ids)
        
        if not users_to_add.exists():
            return Response({"detail": "No valid users found with given IDs"}, status=status.HTTP_400_BAD_REQUEST)

        project.members.add(*users_to_add)

        return Response({
            "message": f"Successfully added {users_to_add.count()} member(s) to the project.",
            "project_id": project.id,
            "members_count": project.members.count()
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def remove_members(self, request, pk=None):
        project = self.get_object()

        if project.created_by != request.user and project.manager != request.user:
            return Response({"detail": "Only project creator or manager can remove members."}, 
                            status=status.HTTP_403_FORBIDDEN)

        member_ids = request.data.get('member_ids', [])
        users_to_remove = User.objects.filter(id__in=member_ids)
        project.members.remove(*users_to_remove)

        return Response({
            "message": f"Successfully removed {users_to_remove.count()} member(s) from the project.",
            "project_id": project.id,
            "members_count": project.members.count()
        }, status=status.HTTP_200_OK)