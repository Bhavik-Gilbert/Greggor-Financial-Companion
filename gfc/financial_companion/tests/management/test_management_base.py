from django.test import TestCase
import sys


class NullOutput(object):
    """
    Redirect all output into nowhere
    """

    def write(self, *args) -> None:
        pass

    def flush(self, *args) -> None:
        pass

class ManagementTestCase(TestCase):
    """
    Base class for testing management commands.
    Call super().setUp() and set
    self.test_model_base to the model to be tested
    in the setUp() method of the subclass.
    """

    def setUp(self):
        super().setUp()
        # redirect stdout into nothing
        self.sysout = sys.stdout
        sys.stdout = NullOutput()

    def tearDown(self):
        # restore stdout
        sys.stdout = self.sysout
