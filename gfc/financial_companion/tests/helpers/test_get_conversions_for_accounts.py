from .test_helper_base import HelperTestCase
from financial_companion.helpers import get_conversions_for_accounts, CurrencyType
from financial_companion.models import BankAccount


class GetConversionsForAccountsHelperFunctionTestCase(HelperTestCase):
    """Test for the get_conversions_for_accounts helpers function"""

    def setUp(self):
        self.valid_bank_accounts = BankAccount.objects.filter(interest_rate__gt=0)
        self.no_valid_bank_accounts = BankAccount.objects.filter(id__lt=0)

    def test_valid_bank_accounts_valid_currency_code(self):
        for currency_code in CurrencyType:
            conversions = get_conversions_for_accounts(self.valid_bank_accounts, currency_code)
            self.assertTrue(currency_code in conversions)
            self.assertEqual(conversions.get(currency_code), 1.0)
            for currency,conversion in conversions.items():   
                self.assertGreater(conversion, 0.0)
    
    def test_valid_bank_accounts_invalid_currency_code(self):
        conversions = get_conversions_for_accounts(self.valid_bank_accounts, "AAA")
        self.assertTrue("AAA" in conversions)
        self.assertEqual(conversions.get("AAA"), 1.0)
        self.assertTrue("GBP" in conversions)
        self.assertEqual(conversions.get("GBP"), 1.0)
        for currency,conversion in conversions.items():   
            self.assertGreater(conversion, 0.0)
    
    def test_no_bank_accounts(self):
        for currency_code in CurrencyType:
            conversions = get_conversions_for_accounts(self.no_valid_bank_accounts, currency_code)
            self.assertTrue(currency_code in conversions)
            self.assertEqual(conversions.get(currency_code), 1.0)
            for currency,conversion in conversions.items():   
                self.assertGreater(conversion, 0.0)