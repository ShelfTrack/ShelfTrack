from django.contrib import admin
from .models import Book, School

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'book_type', 'available_quantity')
    list_filter = ('book_type', 'condition', 'publication_year')
    search_fields = ('title', 'author', 'isbn', 'barcode')
    ordering = ('title',)

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'principal_name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'code', 'principal_name')
    ordering = ('name',) 