from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .student import Student
from .serializers import StudentSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['grade', 'section', 'gender', 'is_active']
    search_fields = ['first_name', 'last_name', 'student_id', 'parent_name']
    ordering_fields = ['grade', 'section', 'first_name', 'last_name', 'admission_date']
    ordering = ['grade', 'section', 'first_name']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            # Only staff and admin can create, update, or delete students
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        """
        Optionally restricts the returned students by filtering against
        query parameters in the URL.
        """
        queryset = Student.objects.all()
        
        # Filter by active status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Filter by grade
        grade = self.request.query_params.get('grade', None)
        if grade is not None:
            queryset = queryset.filter(grade=grade)
        
        # Filter by section
        section = self.request.query_params.get('section', None)
        if section is not None:
            queryset = queryset.filter(section=section.upper())
        
        return queryset 