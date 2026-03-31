from django.urls import path, include
from rest_framework.routers import DefaultRouter
from project.views import ProjectViewSet

router = DefaultRouter()
router.register(r'', ProjectViewSet, basename='project')   # This makes /api/projects/

urlpatterns = [
    path('', include(router.urls)),
]