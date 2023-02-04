from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
import os
import random
import string
import time
from datetime import datetime
from financial_companion.helpers import random_filename

def change_filename(instance, filename):
    return os.path.join('user_profile', random_filename(instance, filename))

class User(AbstractUser):
    """User model used for authentication"""

    username: models.CharField = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{1,}$',
            message='Username must consist of @ followed by at least one letter or number'
        )]
    )
    first_name: models.CharField = models.CharField(max_length=50, blank=False)
    last_name: models.CharField = models.CharField(max_length=50, blank=False)
    email: models.EmailField = models.EmailField(unique=True, blank=False)
    bio: models.CharField = models.CharField(max_length=520, blank=True)
    profile_picture: models.ImageField = models.ImageField(upload_to=change_filename, height_field=None, width_field=None, max_length=100,blank=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
