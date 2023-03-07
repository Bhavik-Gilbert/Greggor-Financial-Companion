from .test_model_base import ModelTestCase
from django.db.models.base import ModelBase
from django.utils import timezone
from decimal import Decimal

from ...helpers import CurrencyType
from ...models import AbstractTransaction, Transaction, User, PotAccount


class TransactionModelTestCase(ModelTestCase):
    """Test file for the concrete transaction model class"""

    def setUp(self) -> None:
        super().setUp()
        self.test_model: Transaction = Transaction.objects.get(id=2)
        self.user: User = User.objects.get(id=1)
        self.sender_account: PotAccount = PotAccount.objects.get(id=5)
        self.receiver_account: PotAccount = PotAccount.objects.get(id=6)

    def test_valid_transaction(self):
        self._assert_model_is_valid()

    def test_valid_time_of_transaction(self):
        self.test_model.time_of_transaction = "2023-02-01T16:30:00+00:00"
        self._assert_model_is_valid()

    def test_time_of_transaction_auto_adds_time_if_blank(self):
        self.test_model.time_of_transaction = ""
        self._assert_model_is_valid()

    def test_sender_account_balance_decreases(self):
        self.sender_balance_before_transaction = self.sender_account.balance
        transaction_model: Transaction = Transaction.objects.create(
            title= "New laptop",
            description= "Bought new laptop",
            amount = round(Decimal(2099.99),2),
            currency = CurrencyType.GBP,
            sender_account = self.sender_account,
            receiver_account = self.receiver_account
        )
        self.sender_account.refresh_from_db()
        self.sender_balance_after_transaction = self.sender_account.balance
        self.assertEqual(Decimal(self.sender_balance_before_transaction - transaction_model.amount), self.sender_balance_after_transaction)

    def test_receiver_account_balance_increases(self):
        self.receiver_balance_before_transaction = self.receiver_account.balance
        transaction_model2: Transaction = Transaction.objects.create(
            title= "New case",
            description= "Bought new case",
            amount = round(Decimal(2099.99),2),
            currency = CurrencyType.GBP,
            sender_account = self.sender_account,
            receiver_account = self.receiver_account
        )
        self.receiver_account.refresh_from_db()
        self.receiver_balance_after_transaction = self.receiver_account.balance
        self.assertEqual(Decimal(self.receiver_balance_before_transaction + transaction_model2.amount), self.receiver_balance_after_transaction)
    
