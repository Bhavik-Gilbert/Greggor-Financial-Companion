from .test_helper_base import HelperTestCase
from financial_companion.helpers import CurrencyType, convert_currency
from typing import Any


class ConvertCurrencyHelperFunctionTestCase(HelperTestCase):
    """Test for the convert_currency helpers function"""

    def _assert_convert_currency(
            self, before_amount: float, current_currency_code: str, target_currency_code: str, equal: bool):
        """Assert convert_currency function working with parameters given"""
        after_amount: float = convert_currency(
            before_amount, current_currency_code, target_currency_code)
        self.assertTrue((before_amount == after_amount) is equal)

    def _assert_valid_change_or_error_convert_currency(
            self, before_amount: float, current_currency_code: str, target_currency_code: str, equal: bool = False):
        """Assert convert_currency function working with parameters given or errors raised are expected"""
        assert_convert_currency_args: dict[str, Any] = {
            "before_amount": before_amount,
            "current_currency_code": current_currency_code,
            "target_currency_code": target_currency_code,
            "equal": equal
        }
        error_message: str = "converter not working"
        warning_message: str = "A package in helpers convert_currency is not working"
        self._assert_valid_valid_or_error(
            self._assert_convert_currency,
            error_message,
            warning_message,
            assert_convert_currency_args)

    def test_valid_currencies_supported(self):
        target_currency_code_1: str = CurrencyType.GBP
        target_currency_code_2: str = CurrencyType.USD

        for current_currency_code in CurrencyType:
            if current_currency_code == target_currency_code_1:
                target_currency_code = target_currency_code_2
            else:
                target_currency_code = target_currency_code_1

            before_amount: float = 100
            self._assert_valid_change_or_error_convert_currency(
                before_amount, current_currency_code, target_currency_code)

    def test_valid_GBP_supported_current(self):
        current_currency_code: str = CurrencyType.GBP
        target_currency_code: str = CurrencyType.USD

        before_amount: float = 100
        self._assert_valid_change_or_error_convert_currency(
            before_amount, current_currency_code, target_currency_code)

    def test_valid_GBP_supported_target(self):
        current_currency_code: str = CurrencyType.USD
        target_currency_code: str = CurrencyType.GBP

        before_amount: float = 100
        self._assert_valid_change_or_error_convert_currency(
            before_amount, current_currency_code, target_currency_code)

    def test_valid_USD_supported_current(self):
        current_currency_code: str = CurrencyType.USD
        target_currency_code: str = CurrencyType.EUR

        before_amount: float = 100
        self._assert_valid_change_or_error_convert_currency(
            before_amount, current_currency_code, target_currency_code)

    def test_valid_USD_supported_target(self):
        current_currency_code: str = CurrencyType.EUR
        target_currency_code: str = CurrencyType.USD

        before_amount: float = 100
        self._assert_valid_change_or_error_convert_currency(
            before_amount, current_currency_code, target_currency_code)

    def test_valid_EUR_supported_current(self):
        current_currency_code: str = CurrencyType.EUR
        target_currency_code: str = CurrencyType.GBP

        before_amount: float = 100
        self._assert_valid_change_or_error_convert_currency(
            before_amount, current_currency_code, target_currency_code)

    def test_valid_EUR_supported_target(self):
        current_currency_code: str = CurrencyType.GBP
        target_currency_code: str = CurrencyType.EUR

        before_amount: float = 100
        self._assert_valid_change_or_error_convert_currency(
            before_amount, current_currency_code, target_currency_code)

    def test_valid_KZT_supported_current(self):
        current_currency_code: str = CurrencyType.KZT
        target_currency_code: str = CurrencyType.GBP

        before_amount: float = 100
        self._assert_valid_change_or_error_convert_currency(
            before_amount, current_currency_code, target_currency_code)

    def test_valid_KZT_supported_target(self):
        current_currency_code: str = CurrencyType.GBP
        target_currency_code: str = CurrencyType.KZT

        before_amount: float = 100
        self._assert_valid_change_or_error_convert_currency(
            before_amount, current_currency_code, target_currency_code)

    def test_valid_amount_same_if_same_current_and_target_currency_codes(self):
        current_currency_code: str = CurrencyType.GBP
        target_currency_code: str = CurrencyType.GBP

        before_amount: float = 100
        self._assert_valid_change_or_error_convert_currency(
            before_amount, current_currency_code, target_currency_code, True)
