from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from .views import TaskViewSet, CommentViewSet

# Main router for tasks
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

# Nested router for comments under tasks
tasks_router = NestedSimpleRouter(router, r'tasks', lookup='task')
tasks_router.register(r'comments', CommentViewSet, basename='task-comments')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(tasks_router.urls)),
]