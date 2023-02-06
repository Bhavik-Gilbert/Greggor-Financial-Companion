from .test_helper_base import HelperTestCase
from financial_companion.helpers import convert_currency, CurrencyType

class ConverCurrencyHelperFunctionTestCase(HelperTestCase):
    """Test for the convert_currency helpers function"""

    def test_valid_currencies_supported(self):
        target_currency_code_1 = CurrencyType.GBP
        target_currency_code_2 = CurrencyType.USD

        for current_currency_code in CurrencyType:
            if current_currency_code == target_currency_code_1:
                target_currency_code = target_currency_code_2
            else:
                target_currency_code = target_currency_code_1

            before_amount: float = 100 
            after_amount: float = convert_currency(before_amount, current_currency_code, target_currency_code)
            self.assertTrue(before_amount != after_amount)
    
    def test_valid_GBP_supported_current(self):
        current_currency_code = CurrencyType.GBP
        target_currency_code = CurrencyType.USD

        before_amount: float = 100 
        after_amount: float = convert_currency(before_amount, current_currency_code, target_currency_code)
        self.assertTrue(before_amount != after_amount)
    
    def test_valid_GBP_supported_target(self):
        current_currency_code = CurrencyType.USD
        target_currency_code = CurrencyType.GBP

        before_amount: float = 100 
        after_amount: float = convert_currency(before_amount, current_currency_code, target_currency_code)
        self.assertTrue(before_amount != after_amount)
    
    def test_valid_USD_supported_current(self):
        current_currency_code = CurrencyType.USD
        target_currency_code = CurrencyType.EUR

        before_amount: float = 100 
        after_amount: float = convert_currency(before_amount, current_currency_code, target_currency_code)
        self.assertTrue(before_amount != after_amount)
    
    def test_valid_USD_supported_target(self):
        current_currency_code = CurrencyType.EUR
        target_currency_code = CurrencyType.USD

        before_amount: float = 100 
        after_amount: float = convert_currency(before_amount, current_currency_code, target_currency_code)
        self.assertTrue(before_amount != after_amount)
    
    def test_valid_EUR_supported_current(self):
        current_currency_code = CurrencyType.EUR
        target_currency_code = CurrencyType.GBP

        before_amount: float = 100 
        after_amount: float = convert_currency(before_amount, current_currency_code, target_currency_code)
        self.assertTrue(before_amount != after_amount)
    
    def test_valid_EUR_supported_target(self):
        current_currency_code = CurrencyType.GBP
        target_currency_code = CurrencyType.EUR

        before_amount: float = 100 
        after_amount: float = convert_currency(before_amount, current_currency_code, target_currency_code)
        self.assertTrue(before_amount != after_amount)

    def test_valid_KZT_supported_current(self):
        current_currency_code = CurrencyType.KZT
        target_currency_code = CurrencyType.GBP

        before_amount: float = 100 
        after_amount: float = convert_currency(before_amount, current_currency_code, target_currency_code)
        self.assertTrue(before_amount != after_amount)
    
    def test_valid_KZT_supported_target(self):
        current_currency_code = CurrencyType.GBP
        target_currency_code = CurrencyType.KZT

        before_amount: float = 100 
        after_amount: float = convert_currency(before_amount, current_currency_code, target_currency_code)
        self.assertTrue(before_amount != after_amount)
    
    def test_valid_amount_same_if_same_current_and_target_currency_codes(self):
        current_currency_code = CurrencyType.GBP
        target_currency_code = CurrencyType.GBP

        before_amount: float = 100 
        after_amount: float = convert_currency(before_amount, current_currency_code, target_currency_code)
        self.assertEqual(before_amount, after_amount)
