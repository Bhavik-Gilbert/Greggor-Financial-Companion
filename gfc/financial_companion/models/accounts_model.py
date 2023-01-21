from django.db.models import (
    Model,
    CharField
)



class Account(Model):
    #Abstract model for all accounts

    name: CharField = CharField(
        max_length = 50,
        blank = False
    )

    description: CharField = CharField(
        max_length = 500,
        blank = True
    )

