from django.db import models


class Timespan(models.TextChoices):
    """ENUM for generic timespans"""
    DAY: str = "day"
    WEEK: str = "week"
    MONTH: str = "month"
    YEAR: str = "year"


class FilterTransactionType(models.TextChoices):
    """ENUM for filter types"""
    ALL: str = "all"
    SENT: str = "sent"
    RECEIVED: str = "received"

    @staticmethod
    def get_send_list() -> list[str]:
        """Filter list for sent transactions"""
        return [FilterTransactionType.SENT, FilterTransactionType.ALL]

    @staticmethod
    def get_received_list() -> list[str]:
        """Filter list for received transactions"""
        return [FilterTransactionType.ALL, FilterTransactionType.RECEIVED]


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


class AccountType(models.TextChoices):
    """ENUM for transaction types"""
    POT: str = "pot"
    BANK: str = "bank"
    REGULAR: str = "regular"


class ScoreListOrderType(models.TextChoices):
    """ENUM for score list order types"""
    RECENT: str = "recent"
    HIGHEST: str = "highest"


class GreggorTypes(models.TextChoices):
    """ENUM for greggor logo types"""
    DISTRAUGHT: str = "distraught"
    SAD: str = "sad"
    PARTY: str = "party"
    NORMAL: str = "normal"
