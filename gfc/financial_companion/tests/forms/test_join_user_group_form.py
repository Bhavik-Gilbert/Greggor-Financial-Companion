from django import forms
from django.urls import reverse
from typing import Any
from .test_form_base import FormTestCase
from financial_companion.forms import JoinUserGroupForm
from financial_companion.models import User


class JoinUserGroupFormTestCase(FormTestCase):
    """Unit tests of the join user group form"""

    def setUp(self):
        self.url: str = reverse('join_user_group')
        self.form_input: dict[str, Any] = {
            "invite_code": "ABCDEFGH"
        }

    def test_valid_join_user_group_form(self):
        form: JoinUserGroupForm = JoinUserGroupForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form: JoinUserGroupForm = JoinUserGroupForm()
        self._assert_form_has_necessary_fields(
            form,
            'invite_code'
        )

    def test_form_cannot_be_shorter_than_8_characters(self):
        self.form_input['invite_code']: str = "ABCDEF"
        form: JoinUserGroupForm = JoinUserGroupForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_cannot_be_longer_than_8_characters(self):
        self.form_input['invite_code']: str = "ABCDEFGHI"
        form: JoinUserGroupForm = JoinUserGroupForm(data=self.form_input)
        self.assertFalse(form.is_valid())
