from django import forms
from typing import Any

from ..test_base import BaseTestCase


class FormTestCase(BaseTestCase):
    """
    Base class for testing forms.
    Call super().setUp() in the
    setUp() method of the subclass.
    """

    def _assert_form_has_necessary_fields(
            self, form: forms.Form, *fields: Any):
        """Asserts the form has the necessary fields"""
        for field in fields:
            self.assertIn(field, form.fields)
