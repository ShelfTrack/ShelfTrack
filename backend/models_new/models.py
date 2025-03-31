from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Book(models.Model):
    BOOK_TYPE_CHOICES = (
        ('textbook', 'Textbook'),
        ('reference', 'Reference Book'),
        ('magazine', 'Magazine'),
        ('novel', 'Novel'),
        ('other', 'Other'),
    )

    CONDITION_CHOICES = (
        ('new', 'New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    )

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    barcode = models.CharField(max_length=50, unique=True)
    book_type = models.CharField(max_length=20, choices=BOOK_TYPE_CHOICES)
    publisher = models.CharField(max_length=200)
    publication_year = models.PositiveIntegerField(
        validators=[MinValueValidator(1800), MaxValueValidator(2024)]
    )
    edition = models.CharField(max_length=50, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    available_quantity = models.PositiveIntegerField(default=1)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    location = models.CharField(max_length=100)  # Shelf/Row number
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['title', 'author']
        indexes = [
            models.Index(fields=['isbn']),
            models.Index(fields=['barcode']),
            models.Index(fields=['title', 'author']),
        ]

    def __str__(self):
        return f"{self.title} by {self.author}"

    def save(self, *args, **kwargs):
        if not self.barcode:
            # Generate barcode if not provided
            from uuid import uuid4
            self.barcode = str(uuid4())[:8].upper()
        super().save(*args, **kwargs)

    @property
    def is_available(self):
        return self.available_quantity > 0

class School(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10, unique=True)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    website = models.URLField(blank=True)
    principal_name = models.CharField(max_length=100)
    established_date = models.DateField()
    is_active = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='school_logos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"

    def save(self, *args, **kwargs):
        if not self.code:
            # Generate school code if not provided
            from uuid import uuid4
            self.code = str(uuid4())[:6].upper()
        super().save(*args, **kwargs) 