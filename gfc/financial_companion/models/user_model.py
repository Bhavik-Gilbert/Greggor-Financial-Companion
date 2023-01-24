from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
import os
import random
import string
import time
from datetime import datetime

def change_filename(instance, filename):
    file_extension = filename.split('.')[-1]
    #get filename
    # set a random filename  ,  os.path.getmtime(instance)
    filename_strings_to_add = [random.choice(string.ascii_letters), str(datetime.now())]
    filename = '{}.{}'.format(''.join(filename_strings_to_add), file_extension)

    return os.path.join('user_profile', filename)

class User(AbstractUser):
    """User model used for authentication"""

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{1,}$',
            message='Username must consist of @ followed by at least one letter or number'
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    bio = models.CharField(max_length=520, blank=True)
    profile_picture = models.ImageField(upload_to=change_filename, height_field=None, width_field=None, max_length=100,blank=True)
