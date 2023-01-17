from enum import Enum

class MessageType(Enum):
    """ENUM defining bootstrap message types"""
    DANGER: str = "danger"
    SUCCESS: str = "success"
    WARNING: str = "warning"
    INFO: str = "info"
    PRIMARY: str = "primary"
    SECONDARY: str = "secondary"

class Timespan(Enum):
    """ENUM for generic timespans"""
    DAY: str = "day"
    WEEK: str = "week"
    MONTH: str = "month"
    YEAR: str = "year"

class TransactionType(Enum):
    """ENUM for transaction types"""
    INCOME: str = "income"
    EXPENSE: str = "expense"