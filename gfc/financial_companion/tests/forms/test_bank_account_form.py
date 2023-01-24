"""Unit tests of the bank account form."""
from django import forms
from .test_form_base import FormTestCase
from financial_companion.forms import BankAccountForm
from financial_companion.helpers import CurrencyType
from decimal import Decimal

class BankAccountFormTestCase(FormTestCase):
    """Unit tests of the bank account form."""
    def setUp(self):
        self.form_input = {
            "name": "Test Bank",
            "description": "This is a test bank",
            "balance": Decimal("99.99"),
            "currency": CurrencyType.GBP,
            "bank_name": "Best Test Bank",
            "account_number": "12345678",
            "sort_code": "123456",
            "iban": "GB1234567890112345",
            "interest_rate": 0
        }

    def test_valid_form_contains_required_fields(self):
        form = BankAccountForm()
        self._assert_form_has_necessary_fields(
            form,
            "name",
            "description",
            "balance",
            "currency"
        )
    
    def test_valid_form_accepts_valid_input(self):
        form = BankAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form_rejects_blank_name(self):
        self.form_input["name"] = ""
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_valid_form_accepts_blank_description(self):
        self.form_input["description"] = ""
        form = BankAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_valid_form_accepts_balance_zero_decimal_places(self):
        self.form_input["balance"] = Decimal("100")
        form = BankAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_valid_form_accepts_balance_up_to_2_decimal_places(self):
        self.form_input["balance"] = Decimal("99.99")
        form = BankAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_valid_form_accepts_balance_up_to_15_digits(self):
        self.form_input["balance"] = Decimal(f"{'9' * 13}.{'9' * 2}")
        form = BankAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form_rejects_balance_3_or_more_decimal_places(self):
        self.form_input["balance"] = Decimal("99.999")
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_invalid_form_rejects_balance_16_or_more_digits(self):
        self.form_input["balance"] = Decimal(f"{'9' * 14}.{'9' * 2}")
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invalid_form_rejects_blank_balance(self):
        self.form_input["balance"] = ""
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_valid_form_accepts_currency_in_currency_type_enum(self):
        for currency in CurrencyType:
            self.form_input["currency"] = currency
            form = BankAccountForm(data=self.form_input)
            self.assertTrue(form.is_valid())
    
    def test_invalid_form_rejects_currency_not_in_currency_type_enum(self):
        currency = "invalid"
        self.assertNotIn(currency, CurrencyType)
        self.form_input["currency"] = currency
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invalid_form_rejects_blank_currency(self):
        self.form_input["currency"] = ""
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_invalid_form_rejects_blank_bank_name(self):
        self.form_input["bank_name"] = ""
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_valid_form_accepts_account_number_whole_numerics(self):
        self.form_input["account_number"] = "9" * 8
        form = BankAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_valid_form_accepts_account_number_8_digits(self):
        self.form_input["account_number"] = "9" * 8
        form = BankAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form_rejects_account_number_non_whole_numeric_try_string(self):
        self.form_input["account_number"] = "hello"
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invalid_form_rejects_account_number_non_whole_numeric_try_decimal(self):
        self.form_input["account_number"] =  f"9.{'9' * 7}"
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_invalid_form_rejects_account_number_non_whole_numeric_try_punctuation(self):
        self.form_input["account_number"] = "!" * 8
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invalid_form_rejects_account_number_less_than_8_digits(self):
        self.form_input["account_number"] = "9" * 7
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_invalid_form_rejects_account_number_more_than_8_digits(self):
        self.form_input["account_number"] = "9" * 9
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_invalid_form_rejects_blank_account_number(self):
        self.form_input["account_number"] = ""
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_valid_form_accepts_sort_code_whole_numerics(self):
        self.form_input["sort_code"] = "9" * 6
        form = BankAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_valid_form_accepts_sort_code_6_digits(self):
        self.form_input["sort_code"] = "9" * 6
        form = BankAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form_rejects_sort_code_non_whole_numeric_try_string(self):
        self.form_input["sort_code"] = "hello"
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invalid_form_rejects_sort_code_non_whole_numeric_try_decimal(self):
        self.form_input["sort_code"] = f"9.{'9' * 5}"
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_invalid_form_rejects_sort_code_non_whole_numeric_try_punctuation(self):
        self.form_input["sort_code"] = "!" * 6
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_invalid_form_rejects_sort_code_less_than_6_digits(self):
        self.form_input["sort_code"] = "9" * 7
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_invalid_form_rejects_sort_code_more_than_6_digits(self):
        self.form_input["sort_code"] = "9" * 9
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_invalid_form_rejects_sort_code(self):
        self.form_input["sort_code"] = ""
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_valid_form_accepts_blank_iban(self):
        self.form_input["iban"] = ""
        form = BankAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_valid_form_accepts_iban_length_15_or_more(self):
        self.form_input["iban"] = f"GB{'9' * 13}"
        form = BankAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_valid_form_accepts_iban_first_2_chars_country_code_try_string(self):
        self.form_input["iban"] = f"GB{'9' * 15}"
        form = BankAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_valid_form_accepts_iban_length_33_or_less(self):
        self.form_input["iban"] = f"GB{'9' * 31}"
        form = BankAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_invalid_form_rejects_iban_first_2_chars_not_country_code_try_numeric(self):
        self.form_input["iban"] = f"{'9' * 15}"
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_invalid_form_rejects_iban_first_2_chars_not_country_code_try_punctuation(self):
        self.form_input["iban"] = f"!!{'9' * 15}"
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_invalid_form_rejects_iban_length_less_than_15(self):
        self.form_input["iban"] = f"GB{'9' * 12}"
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_invalid_form_rejects_iban_length_more_than_33(self):
        self.form_input["iban"] = f"GB{'9' * 32}"
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_valid_form_accepts_interest_rate_up_to_2_decimal_places(self):
        self.form_input["interest_rate"] = Decimal("99.99")
        form = BankAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_valid_form_accepts_interest_rate_up_to_6_digits(self):
        self.form_input["interest_rate"] = Decimal(f"{'9' * 4}.{'9' * 2}")
        form = BankAccountForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_invalid_form_rejects_interest_rate_more_than_6_digits(self):
        self.form_input["interest_rate"] = Decimal(f"{'9' * 5}.{'9' * 2}")
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_invalid_form_rejects_blank_interest_rate(self):
        self.form_input["interest_rate"] = ""
        form = BankAccountForm(data=self.form_input)
        self.assertFalse(form.is_valid())