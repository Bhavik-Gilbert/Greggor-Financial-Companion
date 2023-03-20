from financial_companion.forms import TargetFilterForm
from financial_companion.models import User
from .test_form_base import FormTestCase
from django.test import TestCase


class TargetFilterFormTestCase(FormTestCase):
    """Test of the target filter form"""

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.form_input = {
            "time": "day",
            "income_or_expense": "income",
            "target_type": "account",
        }

    def test_form_contains_required_fields(self):
        form = TargetFilterForm()
        self._assert_form_has_necessary_fields(
            form,
            "time",
            "income_or_expense",
            "target_type"
        )

    def test_valid_target_filter_form(self):
        form = TargetFilterForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_blank_time(self):
        self.form_input['time'] = ''
        form = TargetFilterForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_blank_income_or_expense(self):
        self.form_input['income_or_expense'] = ''
        form = TargetFilterForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_blank_target_type(self):
        self.form_input['target_type'] = ''
        form = TargetFilterForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_get_time_function(self):
        form = TargetFilterForm(data=self.form_input)
        self.assertTrue(form.get_time(), "day")

    def test_get_income_or_expense_function(self):
        form = TargetFilterForm(data=self.form_input)
        self.assertTrue(form.get_income_or_expense(), "income")

    def test_get_target_type_function(self):
        form = TargetFilterForm(data=self.form_input)
        self.assertTrue(form.get_target_type(), "account")
