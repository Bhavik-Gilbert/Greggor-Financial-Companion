from django.db.models import (
    Model,
    CharField,
    DecimalField,
    ForeignKey,
    CASCADE
)

from .category_model import Category
from .user_model import User
from .accounts_model import PotAccount
from ..helpers import Timespan, TransactionType, CurrencyType

class AbstractTarget(Model):
    """Abstract model for target spending and saving"""

    transaction_type: CharField = CharField(
        choices=TransactionType.choices, max_length=7
    )

    timespan: CharField = CharField(
        choices=Timespan.choices, max_length=5
    )

    amount: DecimalField = DecimalField(
        decimal_places=2, max_digits=15
    )

    currency: CharField = CharField(
        choices=CurrencyType.choices, max_length=5, default=CurrencyType.GBP
    )

    class Meta:
        abstract = True

class CategoryTarget(AbstractTarget):
    """Model for target spending and saving on categories"""

    category_id: ForeignKey = ForeignKey(Category, on_delete=CASCADE)

    class Meta:
        unique_together = ["transaction_type", "timespan", "category_id"]

class UserTarget(AbstractTarget):
    """Model for target spending and saving of users"""

    user_id: ForeignKey = ForeignKey(User, on_delete=CASCADE)

    class Meta:
        unique_together = ["transaction_type", "timespan", "user_id"]

class AccountTarget(AbstractTarget):
    """Model for target spending and saving of users"""

    account_id: ForeignKey = ForeignKey(PotAccount, on_delete=CASCADE)

    class Meta:
        unique_together = ["transaction_type", "timespan", "account_id"]