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
                *transactions,
                *fcmodels.Transaction.objects.filter(
                    sender_account=self)]
        if filter_type in TransactionType.get_received_list():
            transactions = [
                *transactions,
                *fcmodels.Transaction.objects.filter(
                    receiver_account=self)]

        return sorted(
            transactions, key=lambda transaction: transaction.time_of_transaction, reverse=True)

    def __str__(self):
        return str(self.name)

    @staticmethod
    def create_basic_account(account_name: str):
        """Creates and returns an account object with only a name"""
        return Account.objects.create(
            name=account_name
        )

    @staticmethod
    def get_or_create_account(account_name: str, user: User = None):
        """Returns account if it exists or creates a new one"""
        try:
            accounts_list: list[Account] = Account.objects.filter(
                name=account_name).select_subclasses()
            get_account: Account = None

            for account in accounts_list:
                if (account.__class__ == Account) or (
                        account.__class__ == PotAccount and account.user == user):
                    get_account = account
                    break

            if get_account is None:
                get_account = Account.create_basic_account(account_name)

            return get_account
        except Exception:
            return None


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
    
    def get_currency(self):
        return self.currency
    
    def get_balance(self):
        return self.balance
    
    def update_balance(ammount):
        balance = ammount


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
