from django.db.models import (
    Model,
    CharField,
    ForeignKey,
    DecimalField,
    CASCADE
)
from encrypted_fields.fields import EncryptedCharField
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator

from .user_model import User
from ..helpers import CurrencyType

class Account(Model):
    """model for all accounts"""

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

def iban_valid(value):
    s1 = value[0:2]
    if(s1.isnumeric()):
        raise ValidationError("IBAN does not start with a iso-3166 country codes")

class BankAccount(PotAccount):
    bank_name: CharField = CharField(
        max_length = 50,
        blank = False
    )
    account_number: EncryptedCharField = EncryptedCharField(
        blank = False,
        max_length=8,
        validators=[only_int, MinLengthValidator(8, "Account number must be 8 digits long")]
    )
    sort_code: EncryptedCharField = EncryptedCharField(
        max_length=6,
        blank=False,
        validators=[only_int, MinLengthValidator(6, "Sort code must be 6 digits long")]
    )
    iban: EncryptedCharField = EncryptedCharField(
        max_length=33,
        blank=True,
        validators=[MinLengthValidator(15, "Iban must be a minimum of 15 characters long")]
    )
    interest_rate: DecimalField = DecimalField(
        max_digits= 6,
        decimal_places=2,
        default=0.0,
    )
