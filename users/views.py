from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser
from django.contrib.auth import get_user_model

from users.api.serializers import UserRegistrationSerializer, UserSerializer

User = get_user_model()


class UserRegistrationViewSet(viewsets.ViewSet):
    """API for registering new users"""
    permission_classes = [AllowAny]
    parser_classes = [JSONParser]   # Only accept JSON

    def create(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully!",
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """View and manage users - Only for Admin (we can restrict later)"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    # Optional: Only allow Admin to view all users
    def get_permissions(self):
        if self.request.user.role == 'Admin':
            return [IsAuthenticated()]
        return [IsAuthenticated()]  # You can make it stricter later