"""Unit tests of the log in form."""
from django import forms
from .test_form_base import FormTestCase
from financial_companion.forms import UserLogInForm

class LogInFormTestCase(FormTestCase):
    """Unit tests of the log in form."""
    def setUp(self):
        self.form_input = {'username': '@janedoe', 'password': 'Password123'}

    def test_form_contains_required_fields(self):
        form = UserLogInForm()
        self._assert_form_has_necessary_fields(
            form,
            'username',
            'password'
        )
        password_field = form.fields['password']
        self.assertTrue(isinstance(password_field.widget,forms.PasswordInput))

    def test_form_accepts_valid_input(self):
        form = UserLogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_username(self):
        self.form_input['username'] = ''
        form = UserLogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_password(self):
        self.form_input['password'] = ''
        form = UserLogInForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_incorrect_username(self):
        self.form_input['username'] = 'ja'
        form = UserLogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_incorrect_password(self):
        self.form_input['password'] = 'pwd'
        form = UserLogInForm(data=self.form_input)
        self.assertTrue(form.is_valid())
