from django.db.models import (
    Model,
    CharField,
    DecimalField,
    ForeignKey,
    CASCADE
)

from django.core.validators import MinValueValidator
from .category_model import Category
from .user_model import User
from .accounts_model import PotAccount
from ..helpers import Timespan, TransactionType, CurrencyType
from decimal import Decimal
from financial_companion.templatetags import get_completeness


class AbstractTarget(Model):
    """Abstract model for target spending and saving"""

    transaction_type: CharField = CharField(
        choices=TransactionType.choices, max_length=7
    )

    timespan: CharField = CharField(
        choices=Timespan.choices, max_length=5
    )

    amount: DecimalField = DecimalField(
        decimal_places=2, max_digits=15, validators=[MinValueValidator(Decimal('0.01'))]
    )

    currency: CharField = CharField(
        choices=CurrencyType.choices, max_length=5, default=CurrencyType.GBP
    )

    class Meta:
        abstract = True

    def is_complete(self):
        if get_completeness(self) >= 100:
            return True
        else:
            return False

    def is_nearly_complete(self):
        completeness = get_completeness(self)
        if completeness >= 75 and completeness < 100:
            return True
        else:
            return False

    def getModelName(self, plural=False):
        if plural:
            return "targets"
        else:
            return "target"

    def __str__(self):
        return self.getModelName()


class CategoryTarget(AbstractTarget):
    """Model for target spending and saving on categories"""

    category: ForeignKey = ForeignKey(Category, on_delete=CASCADE)

    class Meta:
        unique_together = ["transaction_type", "timespan", "category"]

    def getModelName(self, plural=False):
        if plural:
            return "categories"
        else:
            return "category"

    def __str__(self):
        return self.category.name


class UserTarget(AbstractTarget):
    """Model for target spending and saving of users"""

    user: ForeignKey = ForeignKey(User, on_delete=CASCADE)

    class Meta:
        unique_together = ["transaction_type", "timespan", "user"]

    def getModelName(self, plural=False):
        if plural:
            return "users"
        else:
            return "user"

    def __str__(self):
        return "personal target"


class AccountTarget(AbstractTarget):
    """Model for target spending and saving of users"""

    account: ForeignKey = ForeignKey(PotAccount, on_delete=CASCADE)

    class Meta:
        unique_together = ["transaction_type", "timespan", "account"]

    def getModelName(self, plural=False):
        if plural:
            return "accounts"
        else:
            return "accounts"

    def __str__(self):
        return self.account.name
