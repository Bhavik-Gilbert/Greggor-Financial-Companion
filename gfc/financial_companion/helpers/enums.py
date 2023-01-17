from enum import Enum

class MessageType(Enum):
    """ENUM defining bootstrap message types"""
    DANGER = "danger"
    SUCCESS = "success"
    WARNING = "warning"
    INFO = "info"
    PRIMARY = "primary"
    SECONDARY = "secondary"