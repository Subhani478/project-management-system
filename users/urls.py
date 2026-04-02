from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegistrationViewSet, UserViewSet

router = DefaultRouter()

# Register ViewSet for listing and managing users (protected)
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    # Public registration endpoint
    path('register/', UserRegistrationViewSet.as_view({'post': 'create'}), name='register'),
    
    # Include router for other user operations
    path('', include(router.urls)),
]