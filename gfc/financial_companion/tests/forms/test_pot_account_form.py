"""Unit tests of the pot account form."""
from .test_form_base import FormTestCase
from financial_companion.forms import PotAccountForm, MonetaryAccountForm
from financial_companion.helpers import CurrencyType, MonetaryAccountType
from financial_companion.models import User
from decimal import Decimal

class PotAccountFormTestCase(FormTestCase):
    """Unit tests of the pot account form."""
    def setUp(self):
        self.form_input = {
            "name": "Test Pot",
            "description": "This is a test pot",
            "balance": Decimal("99.99"),
            "currency": CurrencyType.GBP
        }

    def test_valid_form_contains_required_fields(self):
        form = PotAccountForm()
        self._assert_form_has_necessary_fields(
            form,
            "name",
            "description",
            "balance",
            "currency"
        )

    def test_get_correct_monetary_account_form_pot_account_form(self):
        user = User.objects.all()[0]
        form = MonetaryAccountForm(form_type = MonetaryAccountType.POT, user=user)
        self.assertIsInstance(form, PotAccountForm)
    
    def test_get_incorrect_monetary_account_form_pot_account_form(self):
        user = User.objects.all()[0]
        form = MonetaryAccountForm(form_type = MonetaryAccountType.BANK, user=user)
        self.assertNotIsInstance(form, PotAccountForm)
    
    def test_valid_form_accepts_valid_input(self):
        form = PotAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form_rejects_blank_name(self):
        self.form_input["name"] = ""
        form = PotAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_valid_form_accepts_blank_description(self):
        self.form_input["description"] = ""
        form = PotAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_valid_form_accepts_balance_zero_decimal_places(self):
        self.form_input["balance"] = Decimal("100")
        form = PotAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_valid_form_accepts_balance_up_to_2_decimal_places(self):
        self.form_input["balance"] = Decimal("99.99")
        form = PotAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_valid_form_accepts_balance_up_to_15_digits(self):
        self.form_input["balance"] = Decimal(f"{'9' * 13}.{'9' * 2}")
        form = PotAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form_rejects_balance_3_or_more_decimal_places(self):
        self.form_input["balance"] = Decimal("99.999")
        form = PotAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_invalid_form_rejects_balance_16_or_more_digits(self):
        self.form_input["balance"] = Decimal(f"{'9' * 14}.{'9' * 2}")
        form = PotAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invalid_form_rejects_blank_balance(self):
        self.form_input["balance"] = ""
        form = PotAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_valid_form_accepts_currency_in_currency_type_enum(self):
        for currency in CurrencyType:
            self.form_input["currency"] = currency
            form = PotAccountForm(data=self.form_input)
            self.assertTrue(form.is_valid())
    
    def test_invalid_form_rejects_currency_not_in_currency_type_enum(self):
        currency = "invalid"
        self.assertNotIn(currency, CurrencyType)
        self.form_input["currency"] = currency
        form = PotAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invalid_form_rejects_blank_currency(self):
        self.form_input["currency"] = ""
        form = PotAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())