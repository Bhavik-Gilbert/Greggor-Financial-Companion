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
        self.transaction_model: Transaction = Transaction()
        self.transaction_model.title= "New laptop"
        self.transaction_model.description= "Bought new laptop"
        self.transaction_model.amount = round(Decimal(2099.99),2)
        self.transaction_model.currency = CurrencyType.GBP
        self.transaction_model.sender_account = self.sender_account
        self.transaction_model.receiver_account = self.receiver_account

    def test_valid_transaction(self):
        self._assert_model_is_valid()

    def test_valid_time_of_transaction(self):
        self.test_model.time_of_transaction = "2023-02-01T16:30:00+00:00"
        self._assert_model_is_valid()

    def test_time_of_transaction_auto_adds_time_if_blank(self):
        self.test_model.time_of_transaction = ""
        self._assert_model_is_valid()

    def test_sender_account_balance_decreases_on_create_transaction(self):
        self.sender_balance_before_transaction = self.sender_account.balance
        self.transaction_model.save()
        self.sender_account.refresh_from_db()
        self.sender_balance_after_transaction = self.sender_account.balance
        self.assertEqual(Decimal(self.sender_balance_before_transaction - self.transaction_model.amount), self.sender_balance_after_transaction)

    def test_receiver_account_balance_increases_on_create_transaction(self):
        self.receiver_balance_before_transaction = self.receiver_account.balance
        self.transaction_model.save()
        self.receiver_account.refresh_from_db()
        self.receiver_balance_after_transaction = self.receiver_account.balance
        self.assertEqual(Decimal(self.receiver_balance_before_transaction + self.transaction_model.amount), self.receiver_balance_after_transaction)
    
    def test_sender_account_balance_increases_on_edit_transaction(self):
        self.transaction_model.save()
        self.sender_account.refresh_from_db()
        self.sender_balance_before_transaction = self.sender_account.balance
        self.old_transaction_amount = self.transaction_model.amount
        self.transaction_model.amount = round(Decimal(1800.00),2)
        self.transaction_model.save()
        self.sender_account.refresh_from_db()
        self.new_transaction_amount = self.transaction_model.amount
        self.sender_balance_after_transaction = self.sender_account.balance
        self.transaction_amount_diff = round(Decimal(self.old_transaction_amount - self.new_transaction_amount),2)
        self.assertEqual(Decimal(self.sender_balance_before_transaction + self.transaction_amount_diff), self.sender_balance_after_transaction)

    def test_sender_account_balance_decreases_on_edit_transaction(self):
        self.transaction_model.save()
        self.sender_account.refresh_from_db()
        self.sender_balance_before_transaction = self.sender_account.balance
        self.old_transaction_amount = self.transaction_model.amount
        self.transaction_model.amount = round(Decimal(2800.00),2)
        self.transaction_model.save()
        self.sender_account.refresh_from_db()
        self.new_transaction_amount = self.transaction_model.amount
        self.sender_balance_after_transaction = self.sender_account.balance
        self.transaction_amount_diff = round(Decimal(self.old_transaction_amount - self.new_transaction_amount),2)
        self.assertEqual(Decimal(self.sender_balance_before_transaction + self.transaction_amount_diff), self.sender_balance_after_transaction)

    def test_receiver_account_balance_increases_on_edit_transaction(self):
        self.transaction_model.save()
        self.receiver_account.refresh_from_db()
        self.receiver_balance_before_transaction = self.receiver_account.balance
        self.old_transaction_amount = self.transaction_model.amount
        self.transaction_model.amount = round(Decimal(1800.00),2)
        self.transaction_model.save()
        self.receiver_account.refresh_from_db()
        self.new_transaction_amount = self.transaction_model.amount
        self.receiver_balance_after_transaction = self.receiver_account.balance
        self.transaction_amount_diff = round(Decimal(self.old_transaction_amount - self.new_transaction_amount),2)
        self.assertEqual(Decimal(self.receiver_balance_before_transaction - self.transaction_amount_diff), self.receiver_balance_after_transaction)

    def test_receiver_account_balance_decreases_on_edit_transaction(self):
        self.transaction_model.save()
        self.receiver_account.refresh_from_db()
        self.receiver_balance_before_transaction = self.receiver_account.balance
        self.old_transaction_amount = self.transaction_model.amount
        self.transaction_model.amount = round(Decimal(2800.00),2)
        self.transaction_model.save()
        self.receiver_account.refresh_from_db()
        self.new_transaction_amount = self.transaction_model.amount
        self.receiver_balance_after_transaction = self.receiver_account.balance
        self.transaction_amount_diff = round(Decimal(self.old_transaction_amount - self.new_transaction_amount),2)
        self.assertEqual(Decimal(self.receiver_balance_before_transaction - self.transaction_amount_diff), self.receiver_balance_after_transaction)
    

    
