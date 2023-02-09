from .test_model_base import ModelTestCase
from django.db.models.base import ModelBase
from django.utils import timezone
from decimal import Decimal

from ...helpers import Timespan
from ...models import AbstractTransaction, RecurringTransaction


class RecurringTransactionTestCase(ModelTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.test_model: RecurringTransaction = RecurringTransaction.objects.get(
            id=1)

    def test_valid_recurring_transaction(self):
        self._assert_model_is_valid()

    def test_valid_transaction_start_Date(self):
        self.test_model.start_date = "2023-01-31"
        self._assert_model_is_valid()

    def test_start_date_auto_adds_if_blank(self):
        self.test_model.start_date = ""
        self._assert_model_is_valid()

    def test_end_date_cannot_be_blank(self):
        self.test_model.end_date = ""
        self._assert_model_is_invalid()

    def test_interval_valid(self):
        self.test_model.interval = Timespan.MONTH
        self._assert_model_is_valid()
