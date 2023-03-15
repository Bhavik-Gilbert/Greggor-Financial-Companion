from django.core.exceptions import ValidationError
from django.db.models import Model

from ..test_base import BaseTestCase


class ManagementTestCase(BaseTestCase):
    """
    Base class for testing management commands.
    Call super().setUp() and set
    self.test_model_base to the model to be tested
    in the setUp() method of the subclass.
    """