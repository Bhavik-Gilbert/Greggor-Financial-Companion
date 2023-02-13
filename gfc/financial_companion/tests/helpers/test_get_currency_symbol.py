from .test_helper_base import HelperTestCase
from financial_companion.helpers import get_currency_symbol, CurrencyType


class GetCurrencySymbolHelperFunctionTestCase(HelperTestCase):
    """Test for the get_currency_symbol helpers function"""

    def test_valid_return_symbol_valid_currency_code(self):
        for currency_code in CurrencyType:
            currency_symbol: str = get_currency_symbol(currency_code)
            self.assertNotEqual("", currency_symbol)

    def test_valid_return_pound_for_GBP(self):
        currency_code: str = CurrencyType.GBP
        currency_symbol: str = get_currency_symbol(currency_code)
        self.assertEqual("£", currency_symbol)

    def test_valid_return_dollar_for_USF(self):
        currency_code: str = CurrencyType.USD
        currency_symbol: str = get_currency_symbol(currency_code)
        self.assertEqual("$", currency_symbol)

    def test_valid_return_euro_for_EUR(self):
        currency_code: str = CurrencyType.EUR
        currency_symbol: str = get_currency_symbol(currency_code)
        self.assertEqual("€", currency_symbol)

    def test_invalid_return_empty_for_invalid_currency_code(self):
        currency_code: str = "not valid"
        self.assertFalse(currency_code in CurrencyType)
        currency_symbol: str = get_currency_symbol(currency_code)
        self.assertEqual("", currency_symbol)

    def test_valid_function_accepts_lower_case_for_currency_code(self):
        currency_code: str = CurrencyType.GBP
        self.assertTrue(currency_code in CurrencyType)
        currency_symbol: str = get_currency_symbol(currency_code.lower())
        self.assertEqual("£", currency_symbol)

    def test_valid_function_accepts_upper_case_for_currency_code(self):
        currency_code: str = CurrencyType.GBP
        self.assertTrue(currency_code in CurrencyType)
        currency_symbol: str = get_currency_symbol(currency_code.upper())
        self.assertEqual("£", currency_symbol)
