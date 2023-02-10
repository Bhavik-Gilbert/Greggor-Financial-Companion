from .test_model_base import ModelTestCase
from django.db.models.base import ModelBase
from decimal import Decimal

from ...helpers import Timespan
from ...models import LinkRecurringTransaction, Transaction, RecurringTransaction


class LinkRecurringTransactionTestCase(ModelTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.test_model: LinkRecurringTransaction = LinkRecurringTransaction.objects.get(
            id=1)

    def test_valid_recurring_transaction(self):
        self._assert_model_is_valid()

    def test_transaction_ofinstance_transaction(self):
        self.assertTrue(isinstance(self.test_model.transaction, Transaction))

    def test_recurring_transaction_ofinstance_recurring_transaction(self):
        self.assertTrue(isinstance(self.test_model.recurring_transaction, RecurringTransaction))
        
         
            
