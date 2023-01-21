from django.db import models

class MessageType(models.TextChoices):
    """ENUM defining bootstrap message types"""
    DANGER: str = "danger"
    SUCCESS: str = "success"
    WARNING: str = "warning"
    INFO: str = "info"
    PRIMARY: str = "primary"
    SECONDARY: str = "secondary"

class Timespan(models.TextChoices):
    """ENUM for generic timespans"""
    DAY: str = "day"
    WEEK: str = "week"
    MONTH: str = "month"
    YEAR: str = "year"

class TransactionType(models.TextChoices):
    """ENUM for transaction types"""
    INCOME: str = "income"
    EXPENSE: str = "expense"

class MonetaryAccountType(models.TextChoices):
    """ENUM for transaction types"""
    POT: str = "pot"
    BANK: str = "bank"

class CurrencyType(models.TextChoices):
    """ENUM for supported currency types"""
    UNITEDSTATESDOLLAR: str = "USD"
    BRITISHPOUND: str = "GBP"
    EURO: str = "EUR"