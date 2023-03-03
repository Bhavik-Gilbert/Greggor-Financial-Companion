from ..test_base import BaseTestCase
from typing import Any
import warnings

class HelperTestCase(BaseTestCase):
    """
    Base class for testing helpers.
    Call super().setUp() in the
    setUp() method of the subclass.
    """

    def _assert_valid_valid_or_error(self, assert_function: callable, expected_error_message: str, warning_message: str, kwargs: dict[Any, Any]):
        """
        Asserts assert function is valid, or expected errors raised
        USAGE:
        _assert_valid_valid_or_error(
            assert_function as function or lambda,
            error_message as string,
            warning_message as string,
            kwargs as dict of values used in assert_function
        )
        kwargs is unwrapped for assert_function, use as direct parameter rather than kwargs
        """
        try:
            assert_function(**kwargs)
        except Exception as error:
            warnings.warn(f"Warning: {warning_message}")
            if not(isinstance(error, Exception) and expected_error_message in str(error).lower()):
                raise Exception(error)