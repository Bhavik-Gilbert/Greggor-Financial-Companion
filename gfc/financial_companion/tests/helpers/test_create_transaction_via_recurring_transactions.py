from .test_helper_base import HelperTestCase
from financial_companion.helpers import create_transaction_via_recurring_transactions
from financial_companion.models import Transaction
from ...models import Transaction
from freezegun import freeze_time


class CreateTransactionViaRecurringTransactionsTaskTestCase(HelperTestCase):
    """Test file for the create transaction via recurring transactions task"""

    def _assert_transaction_count_changes(self, difference=0):
        """Assert that the number of transactions change"""
        before_transaction_count: int = Transaction.objects.all().count()
        create_transaction_via_recurring_transactions()
        after_transaction_count: int = Transaction.objects.all().count()
        self.assertEqual(
            before_transaction_count +
            difference,
            after_transaction_count)

    @freeze_time("2023-01-09 00:00:00")
    def test_valid_create_transaction_via_recurring_transactions(self):
        self._assert_transaction_count_changes(1)

    @freeze_time("2023-01-10 00:00:00")
    def test_valid_no_transactions_made_when_not_on_interval(self):
        self._assert_transaction_count_changes(0)

    @freeze_time("2021-01-10 00:00:00")
    def test_valid_no_transactions_made_when_before_start_date_interval(self):
        self._assert_transaction_count_changes(0)

    @freeze_time("2031-01-10 00:00:00")
    def test_valid_no_transactions_made_when_after_end_date_interval(self):
        self._assert_transaction_count_changes(0)
