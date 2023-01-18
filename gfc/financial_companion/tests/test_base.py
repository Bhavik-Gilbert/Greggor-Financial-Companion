from django.test import TestCase

class BaseTestCase(TestCase):
    """
    Base class for testing.
    Call super().setUp() and set
    self.test_base to the model to be tested
    in the setUp() method of the subclass.
    """

    def setUp(self) -> None:
        pass