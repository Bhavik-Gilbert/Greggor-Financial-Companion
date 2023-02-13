from django.db import models
from .user_model import User

class Category(models.Model):
    """Category model used for different spending categories"""
    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    name: models.ForeignKey = models.CharField(max_length=50, blank=False)
    description: models.CharField = models.CharField(max_length=520, blank=False)
    