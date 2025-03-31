from rest_framework import serializers
from .student import Student

class StudentSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Student
        fields = [
            'id', 'first_name', 'last_name', 'student_id', 'date_of_birth',
            'gender', 'grade', 'section', 'admission_date', 'parent_name',
            'parent_phone', 'parent_email', 'address', 'profile_picture',
            'is_active', 'created_at', 'updated_at', 'age'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_student_id(self, value):
        """
        Check that the student ID is unique
        """
        if Student.objects.filter(student_id=value).exists():
            raise serializers.ValidationError("A student with this ID already exists.")
        return value

    def validate(self, data):
        """
        Check that the grade and section are valid
        """
        if 'grade' in data and (data['grade'] < 1 or data['grade'] > 12):
            raise serializers.ValidationError("Grade must be between 1 and 12")
        
        if 'section' in data and not data['section'].isalpha():
            raise serializers.ValidationError("Section must be a letter")
        
        return data 