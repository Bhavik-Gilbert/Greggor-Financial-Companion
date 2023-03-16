from django import forms
from django.contrib.auth.hashers import check_password
from django.urls import reverse
from typing import Any
from .test_form_base import FormTestCase
from financial_companion.forms import UserChangePasswordForm
from financial_companion.models import User


class UserChangePasswordFormTestCase(FormTestCase):
    """Unit tests of the change password form"""

    def setUp(self):
        self.url: str = reverse('change_password')
        self.form_input: dict[str, Any] = {
            "password": "Password123",
            "new_password": "Password1234"
        }

    def test_form_contains_required_fields(self):
        form: UserChangePasswordForm = UserChangePasswordForm()
        self._assert_form_has_necessary_fields(
            form,
            'password',
            'new_password'
        )
        password_field: forms.Field.CharField = form.fields['password']
        new_password_field: forms.Field.CharField = form.fields['new_password']
        self.assertTrue(isinstance(password_field.widget, forms.PasswordInput))
        self.assertTrue(
            isinstance(
                new_password_field.widget,
                forms.PasswordInput))

    def test_form_accepts_valid_input(self):
        form: UserChangePasswordForm = UserChangePasswordForm(
            data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_password(self):
        self.form_input['password']: str = ''
        form: UserChangePasswordForm = UserChangePasswordForm(
            data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_new_password(self):
        self.form_input['new_password']: str = ''
        form: UserChangePasswordForm = UserChangePasswordForm(
            data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_must_contain_uppercase_character(self):
        self.form_input['new_password']: str = 'password123'
        form: UserChangePasswordForm = UserChangePasswordForm(
            data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_must_contain_lowercase_character(self):
        self.form_input['new_password']: str = 'PASSWORD123'
        form: UserChangePasswordForm = UserChangePasswordForm(
            data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_must_contain_number(self):
        self.form_input['new_password']: str = 'PasswordABC'
        form: UserChangePasswordForm = UserChangePasswordForm(
            data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        user: User = User.objects.get(username='@johndoe')
        form: UserChangePasswordForm = UserChangePasswordForm(
            data=self.form_input)
        old_password: str = user.password
        before_count: int = User.objects.count()
        form.save(instance=user)
        new_password: str = user.password
        after_count: int = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertNotEqual(old_password, new_password)
