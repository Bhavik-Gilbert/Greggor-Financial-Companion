from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    DecimalField,
    CASCADE
)

from .user_model import User
from ..helpers.enums import CurrencyType

class Account(Model):
    #Abstract model for all accounts

    name: CharField = CharField(
        max_length = 50,
        blank = False
    )
    description: CharField = CharField(
        max_length = 500,
        blank = True
    )

class PotAccount(Account):
    user_id: ForeignKey = ForeignKey(User, on_delete=CASCADE)
    balance: DecimalField = DecimalField(max_digits = 15, decimal_places=2)
    currency: CharField = CharField(
        choices=CurrencyType.choices,
        default=CurrencyType.GBP,
        max_length=3
    )

class BankAccount(PotAccount):
    bank_name: CharField = CharField(
        max_length = 50,
        blank = False
    )
    account_number: CharField = CharField(
        blank = False,
        max_length=8
    )
    sort_code: CharField = CharField(
        max_length=6,
        blank=False
    )
    iban: CharField = CharField(
        max_length=34,
        blank=True
    )