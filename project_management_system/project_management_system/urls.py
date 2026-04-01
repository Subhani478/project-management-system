from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT Authentication URLs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),      # Login
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),    # Refresh token
    
    # Apps URL's
    path('api/', include('users.urls')),
    path('api/projects/', include('project.urls')),
    path('api/', include('task.urls')),
]