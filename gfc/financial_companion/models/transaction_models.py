from django.db.models import (
    Model,
    CharField,
    DecimalField,
    FileField,
    DateTimeField,
    DateField,
    ForeignKey,
    ManyToManyField,
    CASCADE, SET_NULL
)

from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from .accounts_model import Account, PotAccount
from .category_model import Category
from .user_model import User
from ..helpers import CurrencyType, Timespan, random_filename, timespan_map
import datetime
import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from decimal import Decimal
from django.db.models import Q
from financial_companion.models import User


def change_filename(instance, filename: str) -> str:
    return os.path.join('transactions', random_filename(filename))


class AbstractTransaction(Model):
    """Abstract model for recording a transaction"""

    title: CharField = CharField(
        blank=False,
        max_length=30
    )

    description: CharField = CharField(
        blank=True,
        max_length=200
    )

    file: FileField = FileField(
        blank=True,
        upload_to=change_filename
    )

    category: ForeignKey = ForeignKey(
        Category, on_delete=SET_NULL, null=True, blank=True)

    amount: DecimalField = DecimalField(
        blank=False,
        decimal_places=2,
        max_digits=15,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    currency: CharField = CharField(
        blank=False,
        choices=CurrencyType.choices,
        max_length=3,
    )

    sender_account: ForeignKey = ForeignKey(
        Account,
        on_delete=CASCADE,
        related_name="sender_account%(app_label)s_%(class)s_related")

    receiver_account: ForeignKey = ForeignKey(
        Account,
        on_delete=CASCADE,
        related_name="receiver%(app_label)s_%(class)s_related")

    def clean(self):
        super().clean()
        try:
            self.sender_account and self.receiver_account
            check_accounts: bool = PotAccount.objects.filter(
                Q(id=self.sender_account.id) | Q(id=self.receiver_account.id)).count() > 0
            if not check_accounts:
                raise ValidationError(
                    "Both sender and receiver accounts cannot be non monetary accounts")
        except ObjectDoesNotExist:
            raise ValidationError(
                "either sender or receiver account does not exist")

    class Meta:
        abstract: bool = True
        unique_together: list[str] = ['sender_account', 'receiver_account']


class Transaction(AbstractTransaction):
    """ Concrete model for a generic transaction """

    time_of_transaction: DateTimeField = DateTimeField(
        blank=False,
        auto_now_add=True
    )

    @staticmethod
    def get_transactions_from_time_period(
            time_choice: Timespan, user: User, filter_type: str = str("all")) -> list:
        user_transactions: list[Transaction] = user.get_user_transactions(
            filter_type=filter_type)

        timespan_int: int = timespan_map[time_choice]
        start_of_timespan_period: datetime = datetime.datetime.today(
        ) - datetime.timedelta(days=timespan_int)

        filtered_transactions: list[Transaction] = []
        for transaction in user_transactions:
            if ((transaction.time_of_transaction.timestamp(
            ) >= start_of_timespan_period.timestamp()) & (transaction.time_of_transaction.timestamp() <= datetime.datetime.today().timestamp())):
                filtered_transactions = [*filtered_transactions, transaction]
        return filtered_transactions

    @staticmethod
    def get_category_splits(
            transactions: list, user: User) -> dict[str, float]:
        spent_per_category: dict[str, float] = dict()
        for x in transactions:
            if ((x.category is None) or (x.category.user.id != user.id)):
                if (spent_per_category.get("Other") is None):
                    spent_per_category["Other"] = x.amount
                else:
                    spent_per_category.update(
                        {"Other": spent_per_category.get("Other") + x.amount})
            else:
                if ((len(spent_per_category) == 0) or (
                        spent_per_category.get(x.category.name) is None)):
                    spent_per_category[x.category.name] = x.amount
                else:
                    spent_per_category.update(
                        {x.category.name: spent_per_category.get(x.category.name) + x.amount})
        return spent_per_category

    class Meta:
        ordering: list[str] = ['-time_of_transaction']

    def _update_account_balances(self):
        check_object_exists: list[Transaction] = Transaction.objects.filter(
            id=self.id).count() > 0
        send_amount: float = -self.amount
        receive_amount: float = self.amount

        if check_object_exists:
            database_transaction: list[Transaction] = Transaction.objects.get(
                id=self.id)

            if (database_transaction.sender_account.id == self.sender_account.id and
                database_transaction.receiver_account.id == self.receiver_account.id and
                    database_transaction.amount == self.amount):
                return

            if database_transaction.sender_account.id == self.sender_account.id:
                send_amount: float = database_transaction.amount - \
                    Decimal(self.amount)
            else:
                database_sender_account: Account = Account.objects.get_subclass(
                    id=database_transaction.sender_account.id)
                if isinstance(database_sender_account, PotAccount):
                    database_sender_account.update_balance(
                        database_transaction.amount, database_transaction.currency)

            if database_transaction.receiver_account.id == self.receiver_account.id:
                receive_amount: Decimal = Decimal(
                    self.amount) - database_transaction.amount
            else:
                database_receiver_account: Account = Account.objects.get_subclass(
                    id=database_transaction.receiver_account.id)
                if isinstance(database_receiver_account, PotAccount):
                    database_receiver_account.update_balance(
                        -database_transaction.amount, database_transaction.currency)

        sender_account: Account = Account.objects.get_subclass(
            id=self.sender_account.id)
        receiver_account: Account = Account.objects.get_subclass(
            id=self.receiver_account.id)

        if isinstance(sender_account, PotAccount):
            sender_account.update_balance(send_amount, self.currency)
        if isinstance(receiver_account, PotAccount):
            receiver_account.update_balance(receive_amount, self.currency)

    def save(self, *args, **kwargs):
        self._update_account_balances()
        super().save(*args, **kwargs)


@receiver(pre_delete, sender=Transaction,
          dispatch_uid='delete_transaction_signal')
def delete_transaction(sender, instance: Transaction, **kwargs):
    instance.amount = 0
    instance._update_account_balances()


class RecurringTransaction(AbstractTransaction):

    start_date: DateField = DateField(
        blank=False,
    )

    interval: CharField = CharField(
        choices=Timespan.choices,
        max_length=10,
    )

    end_date: DateField = DateField(
        blank=False,
    )

    transactions: ManyToManyField = ManyToManyField(Transaction)

    class Meta:
        ordering: list[str] = ['-interval']

    def add_transaction(self, transaction: Transaction):
        """Add transaction to transaction in recurring transaction"""
        self.transactions.add(transaction)
        self.save()
