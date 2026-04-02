from rest_framework import serializers
from django.contrib.auth import get_user_model
from project.models import Project
from task.api.serializers import TaskSerializer   # Make sure path is correct

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    manager = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True
    )

    members = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        required=False,
        allow_empty=True
    )

    manager_detail = serializers.SerializerMethodField(read_only=True)
    members_detail = serializers.SerializerMethodField(read_only=True)   # ← Will be enhanced
    created_by_detail = serializers.SerializerMethodField(read_only=True)

    tasks = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'start_date',
            'end_date',
            'status',
            'priority',
            'manager',
            'manager_detail',
            'members',
            'members_detail',
            'created_by',
            'created_by_detail',
            'tasks',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def get_manager_detail(self, obj):
        if obj.manager:
            return {
                "id": obj.manager.id,
                "username": obj.manager.username,
                "role": obj.manager.role,
                "department": obj.manager.department
            }
        return None

    # ==================== ENHANCED MEMBERS DETAIL ====================
    def get_members_detail(self, obj):
        members_list = []
        for member in obj.members.all():
            # Get tasks assigned to this member in this project
            assigned_tasks = obj.tasks.filter(assigned_to=member)
            
            task_serializer = TaskSerializer(assigned_tasks, many=True, context=self.context)
            
            members_list.append({
                "id": member.id,
                "username": member.username,
                "role": member.role,
                "department": member.department,
                "assigned_tasks": task_serializer.data,     # ← Added: Their tasks
                "assigned_tasks_count": assigned_tasks.count()
            })
        return members_list

    def get_created_by_detail(self, obj):
        return {
            "id": obj.created_by.id,
            "username": obj.created_by.username,
            "role": obj.created_by.role,
            "department": obj.created_by.department
        }

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)
    
    
    
# Lightweight serializer for listing projects
class ProjectListSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.username', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    members_count = serializers.IntegerField(source='members.count', read_only=True)
    task_count = serializers.IntegerField(read_only=True)   # We'll add this later

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'status',
            'priority',
            'start_date',
            'end_date',
            'manager_name',
            'created_by_name',
            'members_count',
            'task_count',
            'created_at'
        ]