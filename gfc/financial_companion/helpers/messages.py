"""Classes for site messages"""
from .enums import MessageType

class Message:
    """Class for message information"""
    def __init__(self, type: MessageType, message: str):
        self.type: MessageType = type
        self.message: str = message