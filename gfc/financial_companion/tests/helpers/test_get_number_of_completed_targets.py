from .test_helper_base import HelperTestCase
from financial_companion.helpers import get_number_of_completed_targets
from financial_companion.models import User
from freezegun import freeze_time
import datetime

class GetNumberOfCompletedTaregtsHelperFunctionTestCase(HelperTestCase):
    """Test for the get_number_of_completed_targets helpers function"""

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.targets = self.user.get_all_targets()
        self.total = 6  #6 / 7 will be complete at the first time check

    @freeze_time("2023-01-01 13:00:00")
    def test_get_completed_within_day(self):
        completed = get_number_of_completed_targets(self.targets)
        self.assertTrue(completed == self.total)

    @freeze_time("2023-01-03 13:00:00")
    def test_get_completed_after_day(self):
        completed = get_number_of_completed_targets(self.targets)
        self.assertTrue(completed <= self.total)

    @freeze_time("2023-01-06 13:00:00")
    def test_get_completed_within_week(self):
        completed = get_number_of_completed_targets(self.targets)
        self.assertTrue(completed <= self.total)

    @freeze_time("2023-01-11 13:00:00")
    def test_get_completed_after_week(self):
        completed = get_number_of_completed_targets(self.targets)
        self.assertTrue(completed <= self.total)

    @freeze_time("2023-01-22 13:00:00")
    def test_get_completed_within_month(self):
        completed = get_number_of_completed_targets(self.targets)
        self.assertTrue(completed <= self.total)

    @freeze_time("2023-02-03 13:00:00")
    def test_get_completed_after_month(self):
        completed = get_number_of_completed_targets(self.targets)
        self.assertTrue(completed <= self.total)

    @freeze_time("2023-07-09 13:00:00")
    def test_get_completed_within_year(self):
        completed = get_number_of_completed_targets(self.targets)
        self.assertTrue(completed <= self.total)

    @freeze_time("2024-08-26 13:00:00")
    def test_get_completed_after_year(self):
        completed = get_number_of_completed_targets(self.targets)
        self.assertTrue(completed <= self.total)
