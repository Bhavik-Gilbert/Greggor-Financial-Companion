from django import forms
from django.urls import reverse
from typing import Any
from .test_form_base import FormTestCase
from financial_companion.forms import AddUserToUserGroupForm
from financial_companion.models import User


class AddUserToUserGroupFormTestCase(FormTestCase):
    """Unit tests of the add user to user group form"""

    def setUp(self):
        self.url: str = reverse('sign_up')
        self.form_input: dict[str, Any] = {
            "user_email": "john.doe@gfc.org"
        }

    def test_valid_add_user_to_user_group_form(self):
        form: AddUserToUserGroupForm = AddUserToUserGroupForm(
            data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form: AddUserToUserGroupForm = AddUserToUserGroupForm()
        self._assert_form_has_necessary_fields(
            form,
            'user_email'
        )
        email_field: forms.EmailField = form.fields['user_email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
