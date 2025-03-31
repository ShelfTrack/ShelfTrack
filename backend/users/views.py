from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import User
from .serializers import UserSerializer

# Create your views here.

class IsAdminOrSelf(permissions.BasePermission):
    """
    Custom permission to only allow admin users or the users themselves to edit their own profile
    """
    def has_object_permission(self, request, view, obj):
        # Allow admin users to do anything
        if request.user.is_staff or request.user.user_type == 'admin':
            return True
        
        # Allow users to view/edit their own profile
        return obj == request.user

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action in ['create']:
            permission_classes = [permissions.IsAdminUser]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsAdminOrSelf]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
