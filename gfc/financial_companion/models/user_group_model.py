from django.db import models
from financial_companion.models import User

class UserGroup(models.Model):
    """Group model used for different groups"""
    name: models.CharField = models.CharField(max_length=50, blank=False)
    description: models.CharField = models.CharField(
        max_length=500, blank=False)
    owner_email: models.EmailField = models.EmailField(blank=False)
    invite_code: models.CharField = models.CharField(max_length=8, blank=False)
    members: models.ManyToManyField = models.ManyToManyField(User)

    def add_member(self, user):
        self.members.add(user)
    
    def remove_member(self, user):
        self.members.remove(user)

    def is_member(self, user):
        """Returns whether user is in the group"""
        return user in self.members.all()
    
    def members_count(self):
        return self.members.count()