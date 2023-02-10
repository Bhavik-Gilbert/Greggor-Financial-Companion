from django.db import models
from financial_companion.models import User

class Group(models.Model):
    """Group model used for different groups"""
    name: models.CharField = models.CharField(max_length=50, blank=False)
    description: models.CharField = models.CharField(
        max_length=500, blank=False)
    owner: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    members: models.ManyToManyField = models.ManyToManyField(User)
    invite_code: models.CharField = models.CharField(max_length=8, blank=False)

    def add_member(self, user):
        self.members.add(user)
    
    def remove_member(self, user):
        self.members.remove(user)

    def is_member(self, user):
        """Returns whether user is in the group"""
        return user in self.members.all()
    
    def members_count(self):
        return self.members.count()