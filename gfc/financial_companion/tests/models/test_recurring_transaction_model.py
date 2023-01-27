from .test_model_base import ModelTestCase
from django.db.models.base import ModelBase
from django.utils import timezone
from decimal import Decimal

from ...helpers import CurrencyType
from ...models import AbstractTransaction, RecurringTransaction

class RecurringTransactionTestCase(ModelTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.test_model: RecurringTransaction = RecurringTransaction.objects.get(id=1)

    def test_valid_recurring_transaction(self):
        self._assert_model_is_valid()
    