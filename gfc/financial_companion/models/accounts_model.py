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
from django.db.models import Q
from model_utils.managers import InheritanceManager
from decimal import Decimal
from financial_companion.models import User
import financial_companion.models as fcmodels
from ..helpers import CurrencyType, AccountType, FilterTransactionType, convert_currency


class Account(Model):
    """
    Account model used to represent merchants that you can send money to
    """

    name: CharField = CharField(
        max_length=50,
        blank=False
    )
    description: CharField = CharField(
        max_length=500,
        blank=True
    )

    user: ForeignKey = ForeignKey(User, on_delete=CASCADE)

    objects: InheritanceManager = InheritanceManager()

    def _get_transactions_filter_account_type(
            self, new_transactions: list, account_type: str, allow_accounts: bool) -> list:
        """
        Return filtered list of transactions based on account_type

        USAGE
        new_transactions: list of transactions
        account_type: string ("sender" or "receiver")
        allow_accounts: boolean if to allow accounts or use pot accounts
            true if allow accounts
            false if use pot accounts
        """
        transactions: list[fcmodels.Transaction] = []

        if account_type in ["sender", "receiver"]:
            for new_transaction in new_transactions:
                account: Account = getattr(
                    new_transaction, f"{account_type}_account")
                if allow_accounts and Account.objects.filter(
                        id=account.id).count() == 1:
                    transactions: list[fcmodels.Transaction] = [
                        *transactions, new_transaction]
                elif PotAccount.objects.filter(id=account.id).count() == 1:
                    transactions: list[fcmodels.Transaction] = [
                        *transactions, new_transaction]

        return list(set(transactions))

    def get_account_transactions(
            self, filter_type: str = FilterTransactionType.ALL, allow_accounts: bool = False) -> list:
        """Return filtered list of the accounts transactions"""
        transactions: list[fcmodels.Transaction] = []

        if filter_type in FilterTransactionType.get_send_list():
            new_transactions: list[fcmodels.Transaction] = fcmodels.Transaction.objects.filter(
                sender_account=self)
            transactions: list[fcmodels.Transaction] = [
                *
                transactions,
                *
                self._get_transactions_filter_account_type(
                    new_transactions,
                    "sender",
                    allow_accounts)]
        if filter_type in FilterTransactionType.get_received_list():
            new_transactions: list[fcmodels.Transaction] = fcmodels.Transaction.objects.filter(
                receiver_account=self)
            transactions: list[fcmodels.Transaction] = [
                *
                transactions,
                *
                self._get_transactions_filter_account_type(
                    new_transactions,
                    "receiver",
                    allow_accounts)]

        return sorted(
            list(set(transactions)), key=lambda transaction: transaction.time_of_transaction, reverse=True)

    def get_account_recurring_transactions(self) -> list:
        """Returns filtered list of all this accounts RECURRING transactions"""
        transactions: list[fcmodels.RecurringTransaction] = []
        transactions: list[fcmodels.RecurringTransaction] = [
            *transactions,
            *fcmodels.RecurringTransaction.objects.filter(
                Q(sender_account=self) | Q(receiver_account=self))]
        return transactions

    def __str__(self) -> str:
        return str(self.name)

    def get_type(self) -> str:
        """Returns account type"""
        return f"{AccountType.REGULAR}"

    @staticmethod
    def create_basic_account(account_name: str, user: User) -> None:
        """Creates and returns an account object with only a name"""
        return Account.objects.create(
            name=account_name,
            user=user
        )

    @staticmethod
    def get_or_create_account(account_name: str, user: User):
        """Returns account if it exists or creates a new one"""
        try:
            account: list[Account] = Account.objects.get_subclass(
                name=account_name, user=user).first()
        except Exception:
            account: Account = Account.create_basic_account(account_name, user)

        return account


class PotAccount(Account):
    """
    PotAccount model used to represent your own account 
    that you can send to or take money from
    """

    balance: DecimalField = DecimalField(max_digits=15, decimal_places=2)
    currency: CharField = CharField(
        choices=CurrencyType.choices,
        default=CurrencyType.GBP,
        max_length=3
    )

    def get_type(self) -> str:
        """Returns account type"""
        return f"{AccountType.POT}"

    def update_balance(self, amount: float, currency: str):
        """
        Updates the object balance converting it to the account currency
        And saving it in the database
        """
        amount: float = convert_currency(amount, currency, self.currency)
        self.balance += Decimal(amount)
        self.save()


def only_int(value: str) -> None:
    """Raises an error if the input given is not numeric"""
    if (not value.isnumeric()):
        raise ValidationError("value contains characters")


def iban_valid(value: str) -> None:
    """
    Raises an error if the inputs first 2 characters are not alphabetical
    """
    s1: str = value[0:2]
    if (not s1.isalpha()):
        raise ValidationError(
            "IBAN does not start with a iso-3166 country codes")


class BankAccount(PotAccount):
    """
    BankAccount model used to represent your own account 
    that you can send to or take money from
    and be affected by interest
    """

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

    def get_type(self) -> str:
        """Returns account type"""
        return f"{AccountType.BANK}"
