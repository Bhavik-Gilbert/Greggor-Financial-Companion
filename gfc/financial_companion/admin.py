"""Configuration of the admin interface of financial_companion."""

from django.contrib import admin
from .models import  User
# Register your models here.
@admin.register(User)
class User(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    list_display = [
        'username', 'first_name', 'last_name', 'email', 'is_active', 'profile_picture'
    ]