from django.db.models import (
    Model,
    CharField,
    IntegerField,
    DecimalField,
    ImageField,
    DateTimeField,
    DateField,
    ForeignKey,
    CASCADE, SET_NULL
)
from django.core.exceptions import ValidationError
from .accounts_model import Account
from .category_model import Category
from ..helpers import CurrencyType, Timespan, random_filename, timespan_map
from datetime import datetime, date
import os


def change_filename(instance, filename):
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

    image: ImageField = ImageField(
        blank=True,
        height_field=None,
        width_field=None,
        max_length=100,
        upload_to='change_filename'
    )

    category = ForeignKey(Category, on_delete=SET_NULL, null=True, blank=True)

    amount: DecimalField = DecimalField(
        blank=False,
        decimal_places=2,
        max_digits=15,
    )

    currency: CharField = CharField(
        blank=False,
        choices=CurrencyType.choices,
        max_length=3,
    )

    sender_account = ForeignKey(
        Account,
        on_delete=CASCADE,
        related_name="sender_account%(app_label)s_%(class)s_related")
    receiver_account = ForeignKey(
        Account,
        on_delete=CASCADE,
        related_name="reciever%(app_label)s_%(class)s_related")

    class Meta:
        abstract = True
        unique_together = ['sender_account', 'receiver_account']


class Transaction(AbstractTransaction):
    """ Concrete model for a generic transaction """

    time_of_transaction: DateTimeField = DateTimeField(
        blank=False,
        auto_now_add=True
    )

    @staticmethod
    def get_transactions_from_last_week(time_choice):
        transactions = []
        timespan_int = timespan_map[time_choice.timespan]
        start_of_timespan_period = datetime.date.today(
        ) - datetime.timedelta(days=timespan_int)

        filtered_transactions = []
        for transaction in transactions:
            if transaction.time_of_transaction.date() >= start_of_timespan_period:
                filtered_transactions = [*filtered_transactions, transaction]   
        print(filtered_transactions)
        return filtered_transactions
    
    @staticmethod
    def get_category_splits(transactions: list):
        spent_per_category= dict()
        no_of_categories = Category.objects.count()
        for x in transactions:
            if (len(spent_per_category) == 0) | spent_per_category.get(x.category) == None:
                spent_per_category[x.category] = x.amount
            else:
                spent_per_category.update({x.category : spent_per_category.get(x.category) + x.amount })
        print(spent_per_category)
        return spent_per_category

    class Meta:
        ordering = ['-time_of_transaction']


class RecurringTransaction(AbstractTransaction):

    start_date: DateField = DateField(
        blank=False,
        auto_now_add=True,
    )

    interval: CharField = CharField(
        choices=Timespan.choices,
        max_length=10,
    )

    end_date: DateField = DateField(
        blank=False,
    )

    class Meta:
        ordering = ['-interval']


class LinkRecurringTransaction(Model):
    """Model for linking individual transactions with their respective recurring transaction"""

    recurring_transaction = ForeignKey(RecurringTransaction, on_delete=CASCADE)

    transaction = ForeignKey(Transaction, on_delete=CASCADE)
