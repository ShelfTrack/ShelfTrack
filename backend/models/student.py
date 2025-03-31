from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)])
    section = models.CharField(max_length=1)
    admission_date = models.DateField(default=timezone.now)
    parent_name = models.CharField(max_length=200)
    parent_phone = models.CharField(max_length=15)
    parent_email = models.EmailField(blank=True)
    address = models.TextField()
    profile_picture = models.ImageField(upload_to='student_profiles/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['grade', 'section', 'first_name', 'last_name']
        indexes = [
            models.Index(fields=['student_id']),
            models.Index(fields=['grade', 'section']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Grade {self.grade}-{self.section}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def age(self):
        today = timezone.now().date()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        ) 