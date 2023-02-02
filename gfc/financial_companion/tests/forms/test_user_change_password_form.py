from django import forms
from django.contrib.auth.hashers import check_password
from django.urls import reverse

from .test_form_base import FormTestCase
from financial_companion.forms import UserChangePasswordForm
from financial_companion.models import User

class UserChangePasswordFormTestCase(FormTestCase):
    """Test of the sign up form"""

    def setUp(self):
        self.url = reverse('change_password')
        self.form_input = {
            "password": "Password123",
            "new_password": "Password1234"
        }

    def test_form_contains_required_fields(self):
        form = UserChangePasswordForm()
        self._assert_form_has_necessary_fields(
            form,
            'password',
            'new_password'
        )
        password_field = form.fields['password']
        new_password_field = form.fields['new_password']
        self.assertTrue(isinstance(password_field.widget,forms.PasswordInput))
        self.assertTrue(isinstance(new_password_field.widget,forms.PasswordInput))

    def test_form_accepts_valid_input(self):
        form = UserChangePasswordForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_password(self):
        self.form_input['password'] = ''
        form = UserChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_new_password(self):
        self.form_input['new_password'] = ''
        form = UserChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_must_contain_uppercase_character(self):
        self.form_input['new_password'] = 'password123'
        form = UserChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_must_contain_lowercase_character(self):
        self.form_input['new_password'] = 'PASSWORD123'
        form = UserChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_new_password_must_contain_number(self):
        self.form_input['new_password'] = 'PasswordABC'
        form = UserChangePasswordForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        user = User.objects.get(username='@johndoe')
        form = UserChangePasswordForm(data=self.form_input)
        old_password = user.password
        before_count = User.objects.count()
        form.save(instance=user)
        new_password = user.password
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertNotEqual(old_password, new_password)
