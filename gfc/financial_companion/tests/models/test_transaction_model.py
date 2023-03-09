from .test_model_base import ModelTestCase
from django.db.models.base import ModelBase
from django.utils import timezone
from decimal import Decimal

from ...helpers import CurrencyType
from ...models import AbstractTransaction, Transaction


class TransactionModelTestCase(ModelTestCase):
    """Test file for the concrete transaction model class"""

    def setUp(self) -> None:
        super().setUp()
        self.test_model: Transaction = Transaction.objects.get(id=2)

    def test_valid_transaction(self):
        self._assert_model_is_valid()

    def test_valid_time_of_transaction(self):
        self.test_model.time_of_transaction = "2023-02-01T16:30:00+00:00"
        self._assert_model_is_valid()

    def test_time_of_transaction_auto_adds_time_if_blank(self):
        self.test_model.time_of_transaction = ""
        self._assert_model_is_valid()
    
    def test_change_filename(self):
        self.transaction = Transaction.objects.get(id = 1)
        self.assertFalse(change_filename(self.transaction,"test").find("transactions"),  -1)

