from django.test import TestCase

class BaseTestCase(TestCase):
    """
    Base class for testing.
    Setup universally used fixtures and information across tests
    """
    
    fixtures: list[str] = [
        "example_target_category.json"
    ]

    def setUp(self) -> None:
        pass