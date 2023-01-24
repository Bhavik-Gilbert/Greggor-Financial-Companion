from django.db import models
from .user_model import User

class Category(models.Model):
    """Category model used for different spending categories"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=50, blank=False)
    