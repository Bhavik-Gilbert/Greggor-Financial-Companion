from .test_helper_base import HelperTestCase
from financial_companion.helpers import get_number_of_days_in_prev_month
from freezegun import freeze_time
from datetime import datetime
import sys


class GetNumberOfDaysInPrevMonthHelperFunctionTestCase(HelperTestCase):
    """Test for the get_number_of_days_in_prev_month helpers function"""

    @freeze_time("2022-08-04 12:00:00")
    def test_return_days_valid_offset(self):
        """Offset month = Nov '22; Prev Mont = Oct '22"""
        offset = 3
        days = get_number_of_days_in_prev_month(offset)
        self.assertGreater(days, 0)
        self.assertEqual(days, 31)

    @freeze_time("2022-08-04 12:00:00")
    def test_return_days_no_offset(self):
        """Offset month = Aug '22; Prev Mont = July '22"""
        days = get_number_of_days_in_prev_month()
        self.assertGreater(days, 0)
        self.assertEqual(days, 31)

    @freeze_time("2022-08-04 12:00:00")
    def test_return_days_null_offset(self):
        """Offset Month = Aug '22; Prev Mont = July '22"""
        offset = 0
        days = get_number_of_days_in_prev_month(offset)
        self.assertGreater(days, 0)
        self.assertEqual(days, 31)
    
    @freeze_time("2022-08-04 12:00:00")
    def test_return_days_negative_offset(self):
        """Offset Month = May '22; Prev Mont = April '22"""
        offset = -3
        days = get_number_of_days_in_prev_month(offset)
        self.assertGreater(days, 0)
        self.assertEqual(days, 30)