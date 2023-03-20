from .test_helper_base import HelperTestCase
from financial_companion.helpers import get_short_month_names_for_timescale, get_projection_timescale_options
from financial_companion.models import BankAccount
from django.db.models import QuerySet


class GetShortMonthNamesForTimescaleHelperFunctionTestCase(HelperTestCase):
    """Test file for the test_get_short_month_names_for_timescale helpers function"""

    def setUp(self):
        self.valid_bank_accounts: QuerySet[BankAccount] = BankAccount.objects.filter(
            interest_rate__gt=0)
        self.no_bank_accounts: QuerySet[BankAccount] = BankAccount.objects.filter(id__lt=0)
        self.max_timescale_in_months: int = max(
            get_projection_timescale_options().keys())

    def test_return_dates_valid_max_timescale(self):
        timescale_in_months: int = 5
        dates: list[str] = get_short_month_names_for_timescale(
            timescale_in_months)
        self.assertEqual(len(dates), timescale_in_months)

    def test_return_dates_no_max_timescale(self):
        dates: list[str] = get_short_month_names_for_timescale()
        self.assertEqual(len(dates), self.max_timescale_in_months)

    def test_return_dates_null_max_timescale(self):
        timescale_in_months: int = 0
        dates: list[str] = get_short_month_names_for_timescale(
            timescale_in_months)
        self.assertEqual(len(dates), timescale_in_months)

    def test_return_dates_invalid_max_timescale(self):
        dates: list[str] = get_short_month_names_for_timescale(-1)
        self.assertEqual(len(dates), 0)
