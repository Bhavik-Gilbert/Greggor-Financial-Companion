from django.test import TestCase

class BaseTestCase(TestCase):
    """
    Base class for testing.
    Setup universally used fixtures and information across tests
    """
    
    fixtures: list[str] = [
        "example_category.json",
        "example_transactions.json",
        "example_users.json",
        "example_accounts.json",
        "example_targets.json",
    ]
    
    def setUp(self) -> None:
        pass