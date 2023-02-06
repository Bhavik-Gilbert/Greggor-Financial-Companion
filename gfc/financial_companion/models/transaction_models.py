from django.db.models import (
    Model,
    CharField,
    IntegerField,
    DecimalField,
    ImageField,
    DateTimeField,
    DateField,
    ForeignKey,
    CASCADE,SET_NULL
)
from django.core.exceptions import ValidationError
from .accounts_model import Account
from .category_model import Category
from ..helpers import CurrencyType, Timespan, random_filename
import os

def change_filename(instance, filename):
    return os.path.join('transactions', random_filename(filename))

class AbstractTransaction(Model):
    """Abstract model for recording a transaction"""

    title: CharField = CharField(
        blank = False,
        max_length = 30
    )

    description: CharField = CharField(
        blank = True,
        max_length = 200
    )

    image: ImageField = ImageField(
        blank = True,
        height_field = None,
        width_field = None,
        max_length = 100,
        upload_to='change_filename'
    )

    category = ForeignKey(Category, on_delete = SET_NULL, null = True, blank = True)

    amount: DecimalField = DecimalField(
        blank = False,
        decimal_places=2,
        max_digits = 15,
    )

    currency: CharField = CharField(
        blank = False,
        choices = CurrencyType.choices,
        max_length = 3,
    )

    sender_account = ForeignKey(Account, on_delete = CASCADE, related_name ="sender_account%(app_label)s_%(class)s_related")
    receiver_account = ForeignKey(Account, on_delete = CASCADE, related_name="reciever%(app_label)s_%(class)s_related")

    class Meta:
        abstract = True
        unique_together = ['sender_account', 'receiver_account']

class Transaction(AbstractTransaction):
    """ Concrete model for a generic transaction """

    time_of_transaction: DateTimeField = DateTimeField(
        blank = False,
        auto_now_add = True
    )

    class Meta:
        ordering = ['-time_of_transaction']

class RecurringTransaction(AbstractTransaction):

    start_date: DateField = DateField(
        blank = False,
        auto_now_add=True,
    )

    interval: CharField = CharField(
        choices=Timespan.choices,
        max_length= 10,
    )

    end_date: DateField = DateField(
        blank = False,
    )

    class Meta:
        ordering = ['-interval']
