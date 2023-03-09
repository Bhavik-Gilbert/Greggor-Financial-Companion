from .test_model_base import ModelTestCase
from django.db.models.base import ModelBase
from django.utils import timezone
from decimal import Decimal

from ...helpers import CurrencyType
from ...models import Transaction, User, PotAccount


class TransactionModelTestCase(ModelTestCase):
    """Test file for the concrete transaction model class"""

    def _assert_balance_changes_on_transaction_created(self, account: PotAccount):
        balance_before_transaction = account.balance
        self.transaction_model.save()
        account.refresh_from_db()
        balance_after_transaction = account.balance
        if self.transaction_model.sender_account == account:
            self.assertEqual(Decimal(balance_before_transaction - self.transaction_model.amount), balance_after_transaction)
        elif self.transaction_model.receiver_account == account:
            self.assertEqual(Decimal(balance_before_transaction + self.transaction_model.amount), balance_after_transaction)
        else:
            raise Exception("Account not used in transaction")

    def _assert_balance_changes_on_transaction_update(self, account: PotAccount, new_transaction_amount: Decimal):
        self.transaction_model.save()
        account.refresh_from_db()
        balance_before_transaction = account.balance
        old_transaction_amount = self.transaction_model.amount
        self.transaction_model.amount = new_transaction_amount
        self.transaction_model.save()
        account.refresh_from_db()
        self.assertEqual(self.transaction_model.amount, new_transaction_amount)
        balance_after_transaction = account.balance
        transaction_amount_diff = round(Decimal(old_transaction_amount - new_transaction_amount), 2)
        if self.transaction_model.sender_account == account:
            self.assertEqual(Decimal(balance_before_transaction + transaction_amount_diff), balance_after_transaction)
        elif self.transaction_model.receiver_account == account: 
            self.assertEqual(Decimal(balance_before_transaction - transaction_amount_diff), balance_after_transaction)
        else:
            raise Exception("Account not used in transaction")

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
        self._assert_balance_changes_on_transaction_created(self.sender_account)

    def test_receiver_account_balance_increases_on_create_transaction(self):
        self._assert_balance_changes_on_transaction_created(self.receiver_account)
    
    def test_sender_account_balance_increases_on_edit_transaction(self):
        self._assert_balance_changes_on_transaction_update(self.sender_account, round(Decimal(1800.00),2))

    def test_sender_account_balance_decreases_on_edit_transaction(self):
        self._assert_balance_changes_on_transaction_update(self.sender_account, round(Decimal(2800.00),2))

    def test_receiver_account_balance_increases_on_edit_transaction(self):
        self._assert_balance_changes_on_transaction_update(self.receiver_account, round(Decimal(1800.00),2))

    def test_receiver_account_balance_decreases_on_edit_transaction(self):
        self._assert_balance_changes_on_transaction_update(self.receiver_account, round(Decimal(2800.00),2))
    
    def test_account_balances_change_on_delete_transaction(self):
        self.transaction_model.save()
        self.sender_account.refresh_from_db()
        self.receiver_account.refresh_from_db()
        sender_account_balance_before_delete = self.transaction_model.sender_account.balance
        receiver_account_balance_before_delete = self.transaction_model.receiver_account.balance
        transaction_ammount = self.transaction_model.amount
        self.transaction_model.delete()
        self.sender_account.refresh_from_db()
        self.receiver_account.refresh_from_db()
        sender_account_balance_after_delete = self.sender_account.balance
        receiver_account_balance_after_delete = self.receiver_account.balance
        self.assertEqual(sender_account_balance_after_delete, sender_account_balance_before_delete + transaction_ammount)
        self.assertEqual(receiver_account_balance_after_delete, receiver_account_balance_before_delete - transaction_ammount)
