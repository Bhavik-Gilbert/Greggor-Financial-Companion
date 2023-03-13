from .test_helper_base import HelperTestCase
from financial_companion.helpers import functions
from financial_companion.helpers.enums import Timespan
from financial_companion.models import Transaction, User
from ...models import Transaction
from freezegun import freeze_time


class CalculatePercentagesFunctionTestCase(HelperTestCase):
    """Test file for the calculate percentages function"""

    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.get(id=1)

    @freeze_time("2023-01-07 22:00:00")
    def test_valid_percentage_function(self):
        total = Transaction.calculate_total(
            Transaction.get_transactions_from_time_period(
                Timespan.WEEK, self.user))
        categories = Transaction.get_category_splits(
            Transaction.get_transactions_from_time_period(
                Timespan.WEEK, self.user))
        percentages = functions.calculate_percentages(categories, total)
        self.assertEqual(round(list(percentages.values())[0]), 97)
