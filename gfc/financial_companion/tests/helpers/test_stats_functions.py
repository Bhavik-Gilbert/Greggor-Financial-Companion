from .test_helper_base import HelperTestCase
from financial_companion.helpers import functions
from financial_companion.helpers.enums import Timespan 
from financial_companion.models import Transaction, Category
from decimal import Decimal
from ...models import Transaction

class StatisticsFunctionsTestCase(HelperTestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_something(self):
        pass
        # self.assertEqual(Transaction.get_transactions_from_time_period(Timespan.WEEK, 2), 0)
