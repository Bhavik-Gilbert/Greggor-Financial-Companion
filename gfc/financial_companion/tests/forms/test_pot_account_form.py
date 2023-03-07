"""Unit tests of the pot account form."""
from .test_form_base import FormTestCase
from typing import Any
from financial_companion.forms import PotAccountForm, MonetaryAccountForm
from financial_companion.helpers import CurrencyType, AccountType
from financial_companion.models import User
from decimal import Decimal


class PotAccountFormTestCase(FormTestCase):
    """Unit tests of the pot account form."""

    def setUp(self):
        self.form_input: dict[Any] = {
            "name": "Test Pot",
            "description": "This is a test pot",
            "balance": Decimal("99.99"),
            "currency": CurrencyType.GBP
        }

    def test_valid_form_contains_required_fields(self):
        form: PotAccountForm = PotAccountForm()
        self._assert_form_has_necessary_fields(
            form,
            "name",
            "description",
            "balance",
            "currency"
        )

    def test_get_correct_monetary_account_form_pot_account_form(self):
        user: User = User.objects.all()[0]
        form: PotAccountForm = MonetaryAccountForm(
            form_type=AccountType.POT, user=user)
        self.assertIsInstance(form, PotAccountForm)

    def test_get_incorrect_monetary_account_form_pot_account_form(self):
        user: User = User.objects.all()[0]
        form: PotAccountForm = MonetaryAccountForm(
            form_type=AccountType.BANK, user=user)
        self.assertNotIsInstance(form, PotAccountForm)

    def test_valid_form_accepts_valid_input(self):
        form: PotAccountForm = PotAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_invalid_form_rejects_blank_name(self):
        self.form_input["name"]: str = ""
        form: PotAccountForm = PotAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_valid_form_accepts_blank_description(self):
        self.form_input["description"]: str = ""
        form: PotAccountForm = PotAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_valid_form_accepts_balance_zero_decimal_places(self):
        self.form_input["balance"]: Decimal = Decimal("100")
        form: PotAccountForm = PotAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_valid_form_accepts_balance_up_to_2_decimal_places(self):
        self.form_input["balance"]: Decimal = Decimal("99.99")
        form: PotAccountForm = PotAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_valid_form_accepts_balance_up_to_15_digits(self):
        self.form_input["balance"]: Decimal = Decimal(f"{'9' * 13}.{'9' * 2}")
        form: PotAccountForm = PotAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_invalid_form_rejects_balance_3_or_more_decimal_places(self):
        self.form_input["balance"]: Decimal = Decimal("99.999")
        form: PotAccountForm = PotAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invalid_form_rejects_balance_16_or_more_digits(self):
        self.form_input["balance"]: Decimal = Decimal(f"{'9' * 14}.{'9' * 2}")
        form: PotAccountForm = PotAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invalid_form_rejects_blank_balance(self):
        self.form_input["balance"]: Decimal = None
        form: PotAccountForm = PotAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_valid_form_accepts_currency_in_currency_type_enum(self):
        for currency in CurrencyType:
            self.form_input["currency"]: str = currency
            form: PotAccountForm = PotAccountForm(data=self.form_input)
            self.assertTrue(form.is_valid())

    def test_invalid_form_rejects_currency_not_in_currency_type_enum(self):
        currency: str = "invalid"
        self.assertNotIn(currency, CurrencyType)
        self.form_input["currency"]: str = currency
        form: PotAccountForm = PotAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invalid_form_rejects_blank_currency(self):
        self.form_input["currency"]: str = ""
        form: PotAccountForm = PotAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())
