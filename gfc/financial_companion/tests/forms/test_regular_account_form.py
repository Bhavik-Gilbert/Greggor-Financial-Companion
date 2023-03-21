from .test_form_base import FormTestCase
from financial_companion.forms import RegularAccountForm, MonetaryAccountForm
from financial_companion.helpers import AccountType
from financial_companion.models import User
from typing import Any


class RegularAccountFormTestCase(FormTestCase):
    """Unit tests of the regular account form."""

    def setUp(self):
        self.form_input: dict[str, Any] = {
            "name": "Test regular",
            "description": "This is a test regular",
        }

    def test_get_correct_monetary_account_form_regular_account_form(self):
        user: User = User.objects.all()[0]
        form: RegularAccountForm = MonetaryAccountForm(
            form_type=AccountType.REGULAR, user=user)
        self.assertIsInstance(form, RegularAccountForm)

    def test_get_incorrect_monetary_account_form_bank_account_form(self):
        user: User = User.objects.all()[0]
        form: RegularAccountForm = MonetaryAccountForm(
            form_type=AccountType.POT, user=user)
        self.assertNotIsInstance(form, RegularAccountForm)

    def test_valid_form_contains_required_fields(self):
        form: RegularAccountForm = RegularAccountForm()
        self._assert_form_has_necessary_fields(
            form,
            "name",
            "description"
        )

    def test_valid_form_accepts_valid_input(self):
        form: RegularAccountForm = RegularAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_invalid_form_rejects_blank_name(self):
        self.form_input["name"]: str = ""
        form: RegularAccountForm = RegularAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_valid_form_accepts_blank_description(self):
        self.form_input["description"]: str = ""
        form: RegularAccountForm = RegularAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())
