from django.db.models import (
    Model,
    CharField,
    DecimalField
)


from ..helpers.enums import Timespan, TransactionType

class Target(Model):
    """Abstract model for target spending and saving"""

    transaction_type: CharField = CharField(
        choices=TransactionType.choices
    )

    timespan: CharField = CharField(
        choices=Timespan.choices
    )

    amount: DecimalField = DecimalField(
        decimal_places=2
    )

    class Meta:
        abstract = True

