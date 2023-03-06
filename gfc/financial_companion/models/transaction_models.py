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
from .accounts_model import Account, PotAccount
from .category_model import Category
from ..helpers import CurrencyType, Timespan, random_filename
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

    class Meta:
        ordering = ['-time_of_transaction']

    def save(self, *args, **kwargs):
        check_object_exists = Transaction.objects.filter(id=self.id).count() > 0
        send_amount = -self.amount
        receive_amount = self.amount

        if check_object_exists:
            database_transaction = Transaction.objects.get(id=self.id)

            if database_transaction.sender_account == self.sender_account:
                send_amount = database_transaction.amount - self.amount
            else:
                database_sender_account = Account.objects.get_subclass(id=database_transaction.sender_account.id)
                if isinstance(database_sender_account, PotAccount):
                    database_sender_account.update_balance(database_transaction.amount, database_transaction.currency)
                
            if database_transaction.receiver_account == self.receiver_account:
                receive_amount = self.amount - database_transaction.amount
            else:
                database_receiver_account = Account.objects.get_subclass(id=database_transaction.receiver_account.id)
                if isinstance(database_receiver_account, PotAccount):
                    database_receiver_account.update_balance(-database_transaction.amount, database_transaction.currency)
        
        
        sender_account = Account.objects.get_subclass(id=self.sender_account.id)
        receiver_account = Account.objects.get_subclass(id=self.receiver_account.id)

        if isinstance(sender_account, PotAccount):
            sender_account.update_balance(send_amount, self.currency)
        if isinstance(receiver_account, PotAccount):
            receiver_account.update_balance(receive_amount, self.currency)

        super().save(*args, **kwargs)



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
