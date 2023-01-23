from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    DecimalField,
    CASCADE
)
from encrypted_fields.fields import EncryptedCharField
from django.core.exceptions import ValidationError

from .user_model import User
from ..helpers import CurrencyType

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

def only_int(value):
    if(not value.isnumeric()):
        raise ValidationError("value contains characters")

class BankAccount(PotAccount):
    bank_name: CharField = CharField(
        max_length = 50,
        blank = False
    )
    account_number: EncryptedCharField = EncryptedCharField(
        blank = False,
        max_length=8,
        validators=[only_int]
    )
    sort_code: EncryptedCharField = EncryptedCharField(
        max_length=6,
        blank=False,
        validators=[only_int]
    )
    iban: EncryptedCharField = EncryptedCharField(
        max_length=34,
        blank=True
    )