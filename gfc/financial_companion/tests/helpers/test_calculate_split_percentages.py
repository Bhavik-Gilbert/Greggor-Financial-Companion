from .test_helper_base import HelperTestCase
from financial_companion.helpers import functions
from financial_companion.helpers.enums import Timespan
from financial_companion.models import Transaction, User
from ...models import Transaction
from freezegun import freeze_time


class CalculateSplitPercentagesFunctionTestCase(HelperTestCase):
    """Test file for the calculate percentages function"""

    def setUp(self) -> None:
        super().setUp()
        self.user: User = User.objects.get(id=1)

    @freeze_time("2023-01-07 22:00:00")
    def test_valid_percentage_function(self):
        category_amounts: dict[str, float] = Transaction.get_category_splits(
            Transaction.get_transactions_from_time_period(
                Timespan.WEEK, self.user), self.user)
        percentages: dict[str, float] = functions.calculate_split_percentages(
            category_amounts)
        self.assertEqual(round(list(percentages.values())[0]), 96)

    @freeze_time("1999-01-07 22:00:00")
    def test_percentages_with_no_data(self):
        category_amounts: dict[str, float] = Transaction.get_category_splits(
            Transaction.get_transactions_from_time_period(
                Timespan.WEEK, self.user), self.user)
        percentages: dict[str, float] = functions.calculate_split_percentages(
            category_amounts)
        self.assertFalse(bool(percentages))
