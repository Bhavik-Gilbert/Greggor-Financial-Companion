from django.test import TestCase

class BaseTestCase(TestCase):
    """
    Base class for testing.
    Setup universally used fixtures and information across tests
    """
    
    fixtures: list[str] = []

    def setUp(self) -> None:
        pass