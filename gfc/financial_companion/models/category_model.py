from django.db import models


class Category(models.Model):
    """Category model used for different spending categories"""
    name = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=50, blank=False)
    