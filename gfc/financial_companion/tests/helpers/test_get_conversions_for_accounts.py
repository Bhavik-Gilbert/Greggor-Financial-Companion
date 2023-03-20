from .test_helper_base import HelperTestCase
from financial_companion.helpers import get_conversions_for_accounts, CurrencyType
from financial_companion.models import BankAccount
from typing import Union
from django.db.models import QuerySet
from typing import Any


class GetConversionsForAccountsHelperFunctionTestCase(HelperTestCase):
    """Test file for the get_conversions_for_accounts helpers function"""

    def _assert_get_conversions_for_accounts(
            self, bank_accounts: list[BankAccount], currency_code: str):
        """Assert get_conversions_for_accounts function working with parameters given"""
        conversions: dict[str, float] = get_conversions_for_accounts(
            bank_accounts, currency_code)
        self.assertTrue(currency_code in conversions)
        self.assertEqual(conversions.get(currency_code), 1.0)
        for currency, conversion in conversions.items():
            self.assertGreater(conversion, 0.0)

    def _assert_valid_change_or_error_get_conversions_for_accounts(
            self, bank_accounts: list[BankAccount], currency_code: str):
        """Assert get_conversions_for_accounts function working with parameters given or errors raised are expected"""
        assert_get_conversions_for_accounts_args: dict[str, Any] = {
            "bank_accounts": bank_accounts,
            "currency_code": currency_code
        }
        error_message: str = ""
        warning_message: str = "A package in helpers convert_currency is not working"
        self._assert_valid_or_error(
            self._assert_get_conversions_for_accounts,
            error_message,
            warning_message,
            assert_get_conversions_for_accounts_args)

    def setUp(self):
        self.valid_bank_accounts: QuerySet[BankAccount] = BankAccount.objects.filter(
            interest_rate__gt=0)
        self.no_valid_bank_accounts: Union[QuerySet,
                                           list[BankAccount]] = BankAccount.objects.filter(id__lt=0)

    def test_valid_bank_accounts_valid_currency_code(self):
        for currency_code in CurrencyType:
            self._assert_valid_change_or_error_get_conversions_for_accounts(
                self.valid_bank_accounts,
                currency_code
            )

    def test_valid_bank_accounts_invalid_currency_code(self):
        conversions: dict[str, float] = get_conversions_for_accounts(
            self.valid_bank_accounts, "AAA")
        self.assertTrue("AAA" in conversions)
        self.assertEqual(conversions.get("AAA"), 1.0)
        self.assertTrue("GBP" in conversions)
        self.assertEqual(conversions.get("GBP"), 1.0)
        for currency, conversion in conversions.items():
            self.assertGreater(conversion, 0.0)

    def test_no_bank_accounts(self):
        for currency_code in CurrencyType:
            self._assert_valid_change_or_error_get_conversions_for_accounts(
                self.no_valid_bank_accounts,
                currency_code
            )
