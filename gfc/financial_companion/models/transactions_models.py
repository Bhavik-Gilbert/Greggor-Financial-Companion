from django.db.models import (
    Model,
    CharField,
    DecimalField,
    ImageField,
    DateTimeField,
    ForeignKey,
)
from .accounts_model import Account
from datetime import datetime
from ..helpers.enums import CurrencyType

def change_filename(instance, filename):
    existing_filename = filename.split('.')[-1]
    #get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, existing_filename)
    else:
        # set a random filename
        filename_strings_to_add = [random.choice(string.ascii_letters), str(datetime.now())]
        filename = '{}.{}'.format(''.join(filename_strings_to_add),existing_filename)

    return os.path.join('transactions', filename)

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

    #category = models.ForeignKey(### Category ###)

    #time_of_transaction: DateTimeField = DateTimeField(
    #    blank = False,
    #    default = datetime.now()
    #)

    amount: DecimalField = DecimalField(
        blank = False,
        decimal_places=2,
        max_digits = None,
    )

    currency: CharField = CharField(
        blank = False,
        choices = CurrencyType.choices,
        max_length = 3
    )

    sender_account = models.ForeignKey(Account, related_name = "sender_account")
    reciever_account = models.ForeignKey(Account, related_name = "reciever_account")

    class Meta:
        abstract = True
