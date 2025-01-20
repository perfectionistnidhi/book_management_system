from django.contrib import admin
from .models import Book, Genre, CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('role',)

admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(CustomUser, CustomUserAdmin)
