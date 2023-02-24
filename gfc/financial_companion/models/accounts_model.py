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
from model_utils.managers import InheritanceManager

from financial_companion.models import User
import financial_companion.models as fcmodels
from ..helpers import CurrencyType, MonetaryAccountType, TransactionType


class Account(Model):
    """model for all accounts"""

    name: CharField = CharField(
        max_length=50,
        blank=False
    )
    description: CharField = CharField(
        max_length=500,
        blank=True
    )

    objects = InheritanceManager()

    def get_account_transactions(self, filter_type: str = "all") -> list:
        """Return filtered list of the accounts transactions"""
        transactions: list[fcmodels.Transaction] = []

        if filter_type in TransactionType.get_send_list():
            transactions = [
                *
                transactions,
                *
                fcmodels.Transaction.objects.filter(
                    sender_account=self)]
        if filter_type in TransactionType.get_received_list():
            transactions = [
                *
                transactions,
                *
                fcmodels.Transaction.objects.filter(
                    receiver_account=self)]

        return transactions


class PotAccount(Account):
    user: ForeignKey = ForeignKey(User, on_delete=CASCADE)
    balance: DecimalField = DecimalField(max_digits=15, decimal_places=2)
    currency: CharField = CharField(
        choices=CurrencyType.choices,
        default=CurrencyType.GBP,
        max_length=3
    )

    def get_type(self):
        return f"{MonetaryAccountType.POT}"


def only_int(value):
    if (not value.isnumeric()):
        raise ValidationError("value contains characters")


def iban_valid(value):
    s1 = value[0:2]
    if (not s1.isalpha()):
        raise ValidationError(
            "IBAN does not start with a iso-3166 country codes")


class BankAccount(PotAccount):
    bank_name: CharField = CharField(
        max_length=50,
        blank=False
    )
    account_number: EncryptedCharField = EncryptedCharField(
        blank=False,
        max_length=8,
        validators=[only_int, MinLengthValidator(
            8, "Account number must be 8 digits long")]
    )
    sort_code: EncryptedCharField = EncryptedCharField(
        max_length=6,
        blank=False,
        validators=[only_int, MinLengthValidator(
            6, "Sort code must be 6 digits long")]
    )
    iban: EncryptedCharField = EncryptedCharField(
        max_length=33,
        blank=True,
        null=True,
        validators=[iban_valid, MinLengthValidator(
            15, "Iban must be a minimum of 15 characters long")]
    )
    interest_rate: DecimalField = DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.0,
    )

    def get_type(self):
        return f"{MonetaryAccountType.BANK}"
