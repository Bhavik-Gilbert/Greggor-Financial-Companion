from .test_helper_base import HelperTestCase
from financial_companion.helpers import functions
from financial_companion.helpers.enums import Timespan 
from financial_companion.models import Transaction, Category, User
from decimal import Decimal
from datetime import datetime
from ...models import Transaction

class StatisticsFunctionsTestCase(HelperTestCase):

    def setUp(self) -> None:
        super().setUp()
        self.user = User.objects.get(id=1)
        self.transactions = Transaction.objects.filter(sender_account=3)
    
    def _set_transactions_now(self, transactions):
        for transaction in transactions:
            transaction.time_of_transaction = datetime.now()
            transaction.save()

    def test_valid_within_time_period(self):
        self._set_transactions_now(self.transactions)
        self.assertEqual(len(Transaction.get_transactions_from_time_period(Timespan.WEEK, self.user)), 4)

    def test_valid_split_categories(self):
        self._set_transactions_now(self.transactions)
        self.assertEqual(len(Transaction.get_category_splits(Transaction.get_transactions_from_time_period(Timespan.WEEK, self.user))), 1)

    def test_valid_percentage_function(self):
        self._set_transactions_now(self.transactions)
        total = Transaction.calculate_total(Transaction.get_transactions_from_time_period(Timespan.WEEK, self.user))
        categories = Transaction.get_category_splits(Transaction.get_transactions_from_time_period(Timespan.WEEK, self.user))
        percentages = functions.calculate_percentages(categories, total)
        self.assertEqual(list(percentages.values())[0], 100)