"""Classes for site messages"""
from enum import Enum

class MessageType(Enum):
    """ENUM defining bootstrap message types"""
    DANGER = "danger"
    SUCCESS = "success"
    WARNING = "warning"
    INFO = "info"
    PRIMARY = "primary"
    SECONDARY = "secondary"

class Message:
    """Class for message information"""
    def __init__(self, type: MessageType, message: str):
        self.type: MessageType = type
        self.message: str = message