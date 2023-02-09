from django.db import models
from financial_companion.models import User
import financial_companion.models as fcmodels
from ..helpers import TransactionType


class Category(models.Model):
    """Category model used for different spending categories"""
    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    name: models.ForeignKey = models.CharField(max_length=50, blank=False)
    description: models.CharField = models.CharField(
        max_length=520, blank=False)

    def get_category_transactions(self, filter_type: str = "all") -> list:
        """Return filtered list of the categories transactions"""
        return list(set(self.user.get_user_transactions(filter_type)) & set(
            fcmodels.Transaction.objects.filter(category=self)))
