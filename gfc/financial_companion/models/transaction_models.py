from django.db.models import (
    Model,
    CharField,
    IntegerField,
    DecimalField,
    ImageField,
    DateTimeField,
    DateField,
    ForeignKey,
    ManyToManyField,
    CASCADE, SET_NULL
)
from .accounts_model import Account, PotAccount
from .category_model import Category
from ..helpers import CurrencyType, Timespan, random_filename, timespan_map, TransactionType
import datetime
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
        upload_to=change_filename
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
    def calculate_total(transactions: list):
        total = 0
        for x in transactions:
            total += x.amount
        return total


    @staticmethod
    def get_transactions_from_time_period(time_choice, user, filter_type = str("all")):
        user_transactions = user.get_user_transactions(filter_type=filter_type)
        
        timespan_int = timespan_map[time_choice]
        start_of_timespan_period = datetime.datetime.today(
        ) - datetime.timedelta(days=timespan_int)

        filtered_transactions = []
        for transaction in user_transactions:
            if transaction.time_of_transaction.timestamp() >= start_of_timespan_period.timestamp():
                filtered_transactions = [*filtered_transactions, transaction]   
        return filtered_transactions
    
    @staticmethod
    def get_category_splits(transactions: list):
        spent_per_category= dict()
        no_of_categories = Category.objects.count()
        for x in transactions:
            if (x.category is None) :
                if (spent_per_category.get("Other") == None):
                    spent_per_category["Other"] = x.amount
                else:
                    spent_per_category.update({"Other" : spent_per_category.get("Other") + x.amount})
            elif ((len(spent_per_category) == 0) | (spent_per_category.get(x.category.name) == None)):
                spent_per_category[x.category.name] = x.amount
            else:
                spent_per_category.update({x.category.name : spent_per_category.get(x.category.name) + x.amount })
        return spent_per_category

    class Meta:
        ordering = ['-time_of_transaction']


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
        ordering = ['-interval']
    
    def add_transaction(self, transaction: Transaction):
        """Add transaction to transaction in recurring transaction"""
        self.transactions.add(transaction)
        self.save()