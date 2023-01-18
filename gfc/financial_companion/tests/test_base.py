from django.test import TestCase

class BaseTestCase(TestCase):
    """
    Base class for testing.
    Setup universally used fixtures and information across tests
    """

    def __init__(self, methodName: str = "runTest") -> None:
        """Clear database for testing"""
        super().__init__(methodName=methodName)

    fixtures: list[str] = []

    def setUp(self) -> None:
        pass