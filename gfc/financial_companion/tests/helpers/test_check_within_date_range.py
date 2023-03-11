from .test_helper_base import HelperTestCase
from financial_companion.helpers import check_within_date_range
from datetime import date, datetime
from freezegun import freeze_time


class CheckWithinDateRangeHelperFunctionTestCase(HelperTestCase):
    """Test for the check_within_date_range helpers function"""

    def _assert_range_is_invalid(
            self, start_date: date, end_date: date, current_date: date):
        check_range: bool = check_within_date_range(
            start_date, end_date, current_date)
        self.assertFalse(check_range)

    def _assert_range_is_valid(
            self, start_date: date, end_date: date, current_date: date):
        check_range: bool = check_within_date_range(
            start_date, end_date, current_date)
        self.assertTrue(check_range)

    @freeze_time("2023-01-09 00:00:00")
    def test_valid_date_within_range(self):
        current_date: date = date.today()
        start_date: date = datetime(2023, 1, 8).date()
        end_date: date = datetime(2023, 1, 10).date()
        self._assert_range_is_valid(start_date, end_date, current_date)

    @freeze_time("2023-01-09 00:00:00")
    def test_invalid_date_before_start(self):
        current_date: date = date.today()
        start_date: date = datetime(2023, 1, 10).date()
        end_date: date = datetime(2023, 1, 11).date()
        self._assert_range_is_invalid(start_date, end_date, current_date)

    @freeze_time("2023-01-09 00:00:00")
    def test_invalid_date_after_end(self):
        current_date: date = date.today()
        start_date: date = datetime(2023, 1, 7).date()
        end_date: date = datetime(2023, 1, 8).date()
        self._assert_range_is_invalid(start_date, end_date, current_date)

    @freeze_time("2023-01-09 00:00:00")
    def test_valid_start_date_swaps_with_end_date_when_greater_than_start_date(
            self):
        current_date: date = date.today()
        start_date: date = datetime(2023, 1, 10).date()
        end_date: date = datetime(2023, 1, 8).date()
        self._assert_range_is_valid(start_date, end_date, current_date)
