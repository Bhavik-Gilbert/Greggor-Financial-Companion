from .test_helper_base import HelperTestCase
from financial_companion.helpers import generate_random_end_date
from datetime import datetime


class GenerateEndDateTestCase(HelperTestCase):
    """Test file for the generate_random_end_date helpers function"""

    def test_valid_date_time(self):
        random_date: datetime = generate_random_end_date()
        self.assertTrue(isinstance(random_date, datetime))
