
from rest_framework import serializers
from django.contrib.auth import get_user_model
from task.models import Task, Comment
from users.api.serializers import UserSerializer

User = get_user_model()



class TaskSerializer(serializers.ModelSerializer):
    """Serializer for Task model with validation and nested user details."""
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
            "created_at",
            "updated_at"
        ]
        read_only_fields = ["created_at", "updated_at"]

    def get_assigned_to_detail(self, obj):
        if obj.assigned_to:
            return UserSerializer(obj.assigned_to).data
        return None

    def validate(self, attrs):
        start = attrs.get('start_date', getattr(self.instance, 'start_date', None))
        end = attrs.get('end_date', getattr(self.instance, 'end_date', None))
        if start and end and end < start:
            raise serializers.ValidationError({"end_date": "End date must be after start date."})
        return attrs

    def create(self, validated_data):
        # Custom logic can be added here
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Custom logic can be added here
        return super().update(instance, validated_data)



class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment model with content validation and nested author details."""
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'task', 'author', 'content', 'created_at']
        read_only_fields = ['author', 'created_at']

    def validate_content(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Comment content is too short (min 3 characters).")
        return value

    def create(self, validated_data):
        # Custom logic can be added here
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Custom logic can be added here
        return super().update(instance, validated_data)