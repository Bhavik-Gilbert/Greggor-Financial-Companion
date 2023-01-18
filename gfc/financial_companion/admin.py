"""Configuration of the admin interface of financial_companion."""

from django.contrib import admin
from .models import Target

# Register your models here.
admin.site.register(Target)
