from django.contrib import admin
from .student import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'grade', 'section', 'is_active')
    list_filter = ('grade', 'section', 'gender', 'is_active')
    search_fields = ('first_name', 'last_name', 'student_id', 'parent_name')
    ordering = ('grade', 'section', 'first_name', 'last_name')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'student_id', 'date_of_birth',
                      'gender', 'grade', 'section', 'profile_picture')
        }),
        ('Parent Information', {
            'fields': ('parent_name', 'parent_phone', 'parent_email', 'address')
        }),
        ('Status', {
            'fields': ('is_active', 'admission_date')
        })
    ) 