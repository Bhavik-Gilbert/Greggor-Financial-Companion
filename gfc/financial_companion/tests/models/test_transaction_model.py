from .test_model_base import ModelTestCase

from ...models import Transaction
from financial_companion.helpers.enums import Timespan 
from financial_companion.models import Transaction, User
from ...models import Transaction
from freezegun import freeze_time


class TransactionModelTestCase(ModelTestCase):
    """Test file for the concrete transaction model class"""

    def setUp(self) -> None:
        super().setUp()
        self.test_model: Transaction = Transaction.objects.get(id=2)
        self.user = User.objects.get(id=1)
        self.transactions = Transaction.objects.all()
    
    def _set_categories_none(self, transactions):
        for transaction in transactions:
            transaction.category = None
            transaction.save()

    def test_valid_transaction(self):
        self._assert_model_is_valid()

    def test_valid_time_of_transaction(self):
        self.test_model.time_of_transaction = "2023-02-01T16:30:00+00:00"
        self._assert_model_is_valid()

    def test_time_of_transaction_auto_adds_time_if_blank(self):
        self.test_model.time_of_transaction = ""
        self._assert_model_is_valid()
    
    @freeze_time("2023-01-07 22:00:00")
    def test_valid_within_time_period(self):
        self.assertEqual(len(Transaction.get_transactions_from_time_period(Timespan.WEEK, self.user)), 7)

    @freeze_time("2023-01-07 22:00:00")
    def test_valid_split_categories(self):
        self.assertEqual(len(Transaction.get_category_splits(Transaction.get_transactions_from_time_period(Timespan.WEEK, self.user))), 1)

    @freeze_time("2023-01-07 22:00:00")
    def test_valid_split_categories_with_category_none(self):
        self._set_categories_none(self.transactions)
        self.assertEqual(len(Transaction.get_category_splits(Transaction.get_transactions_from_time_period(Timespan.WEEK, self.user))), 1)
