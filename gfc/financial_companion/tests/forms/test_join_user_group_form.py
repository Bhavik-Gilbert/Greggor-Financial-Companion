from django import forms
from django.urls import reverse

from .test_form_base import FormTestCase
from financial_companion.forms import JoinUserGroupForm
from financial_companion.models import User


class JoinUserGroupFormTestCase(FormTestCase):
    """Test of the sign up form"""

    def setUp(self):
        self.url = reverse('join_user_group')
        self.form_input = {
            "invite_code": "ABCDEFGH"
        }

    def test_valid_join_user_group_form(self):
        form = JoinUserGroupForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = JoinUserGroupForm()
        self._assert_form_has_necessary_fields(
            form,
            'invite_code'
        )

    def test_form_cannot_be_shorter_than_8_characters(self):
        self.form_input['invite_code'] = "ABCDEF"
        form = JoinUserGroupForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_cannot_be_longer_than_8_characters(self):
        self.form_input['invite_code'] = "ABCDEFGHI"
        form = JoinUserGroupForm(data=self.form_input)
        self.assertFalse(form.is_valid())
