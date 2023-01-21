from django.core.exceptions import ValidationError
from django.db.models import Model

from ..test_base import BaseTestCase

class ModelTestCase(BaseTestCase):
    """
    Base class for testing models.
    Call super().setUp() and set
    self.test_model_base to the model to be tested
    in the setUp() method of the subclass.
    """

    fixtures: list[str] = ["example_users.json","example_category.json"]

    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName=methodName)
        self.test_model: Model = None

    def _assert_model_is_valid(self) -> None:
        """
        Assert that database constraints are satisfied.
        """

        self._check_model()
        try:
            self.test_model.full_clean()
        except ValidationError:
            self.fail(f"Test {self.test_model.__class__.__name__} should be valid!")

    def _assert_model_is_invalid(self) -> None:
        """
        Assert that database constraints are not satisfied.
        """

        self._check_model()
        with self.assertRaises(ValidationError):
            self.test_model.full_clean()

    def _check_model(self) -> None:
        if self.test_model is None:
            self.fail("self.test_model_base was not set in the test's setUp() method!")
        if not isinstance(self.test_model, Model):
            self.fail(f"self.test_model {self.test_model} is not a Model!")
