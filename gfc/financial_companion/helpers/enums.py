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

class CurrencyType(models.TextChoices):
    """ENUM for currency types"""
    GBP: str = "GBP"
    USD: str = "USD"
    EUR: str = "EUR"
    JPY: str = "JPY"
    CNY: str = "CNY"
    AUD: str = "AUD"
    CAD: str = "CAD"
    INR: str = "INR"
    RUB: str = "RUB"
    NZD: str = "NZD"
    CHF: str = "CHF"
    KZT: str = "KZT"

class MonetaryAccountType(models.TextChoices):
    """ENUM for transaction types"""
    POT: str = "pot"
    BANK: str = "bank"

class GreggorTypes(models.TextChoices):
    """ENUM for greggor logo types"""
    SAD: str = "sad"
    PARTY: str = "party"
    NORMAL: str = "normal"
