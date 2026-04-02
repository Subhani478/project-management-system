from rest_framework import serializers
from django.contrib.auth import get_user_model
from task.models import Task, Comment

User = get_user_model()


class TaskSerializer(serializers.ModelSerializer):
    # This will show assignee's details nicely
    assigned_to_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "project",
            "assigned_to",
            "assigned_to_detail",     
            "start_date",
            "end_date",
            "status",
            "priority",
            "progress",               
            "created_at"
        ]
        read_only_fields = ["created_at"]

    def get_assigned_to_detail(self, obj):
        if obj.assigned_to:
            return {
                "id": obj.assigned_to.id,
                "username": obj.assigned_to.username,
                "full_name": f"{obj.assigned_to.first_name or ''} {obj.assigned_to.last_name or ''}".strip(),
                "role": getattr(obj.assigned_to, 'role', None),
                "department": getattr(obj.assigned_to, 'department', None)
            }
        return None


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'task', 'author', 'content', 'created_at']
        read_only_fields = ['author', 'created_at']