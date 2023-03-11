from .test_helper_base import HelperTestCase
from financial_companion.helpers import check_date_on_interval, Timespan
from datetime import date, datetime
from freezegun import freeze_time


class CheckDateOnIntervalHelperFunctionTestCase(HelperTestCase):
    """Test for the check_date_on_interval helpers function"""

    def _assert_interval_is_invalid(self, interval: Timespan, start_date: date, current_date: date):
        check_interval: bool = check_date_on_interval(interval, start_date, current_date)
        self.assertFalse(check_interval)
    
    def _assert_interval_is_valid(self, interval: Timespan, start_date: date, current_date: date):
        check_interval: bool = check_date_on_interval(interval, start_date, current_date)
        self.assertTrue(check_interval)

    @freeze_time("2023-01-16 00:00:00")
    def test_valid_date_on_interval(self):
        current_date: date = date.today()
        start_date: date = datetime(2023, 1, 9).date()
        interval: Timespan = Timespan.WEEK
        self._assert_interval_is_valid(interval, start_date, current_date)
    
    @freeze_time("2023-01-17 00:00:00")
    def test_invalid_date_not_on_interval(self):
        current_date: date = date.today()
        start_date: date = datetime(2023, 1, 9).date()
        interval: Timespan = Timespan.WEEK
        self._assert_interval_is_invalid(interval, start_date, current_date)
    
    @freeze_time("2023-01-09 00:00:00")
    def test_invalid_current_date_before_start_date(self):
        current_date: date = date.today()
        start_date: date = datetime(2023, 1, 16).date()
        interval: Timespan = Timespan.WEEK
        self._assert_interval_is_invalid(interval, start_date, current_date)
    
