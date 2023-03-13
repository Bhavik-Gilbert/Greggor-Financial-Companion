from .test_model_base import ModelTestCase

from django.db.models.base import ModelBase
from django.utils import timezone
from decimal import Decimal
from financial_companion.models.transaction_models import change_filename
from ...helpers import CurrencyType
from ...models import AbstractTransaction, Transaction, User
from financial_companion.helpers.enums import Timespan
from ...models import Transaction
from financial_companion.helpers.enums import Timespan, CurrencyType
from financial_companion.models import Transaction, User, PotAccount, User
from freezegun import freeze_time
from decimal import Decimal


class TransactionModelTestCase(ModelTestCase):
    """Test file for the concrete transaction model class"""

    def _assert_balance_changes_on_transaction_created(
            self, account: PotAccount):
        balance_before_transaction = account.balance
        self.transaction_model.save()
        account.refresh_from_db()
        balance_after_transaction = account.balance
        if self.transaction_model.sender_account == account:
            self.assertEqual(
                Decimal(
                    balance_before_transaction -
                    self.transaction_model.amount),
                balance_after_transaction)
        elif self.transaction_model.receiver_account == account:
            self.assertEqual(
                Decimal(
                    balance_before_transaction +
                    self.transaction_model.amount),
                balance_after_transaction)
        else:
            raise Exception("Account not used in transaction")

    def _assert_balance_changes_on_transaction_update(
            self, account: PotAccount, new_transaction_amount: Decimal):
        self.transaction_model.save()
        account.refresh_from_db()
        balance_before_transaction = account.balance
        old_transaction_amount = self.transaction_model.amount
        self.transaction_model.amount = new_transaction_amount
        self.transaction_model.save()
        account.refresh_from_db()
        self.assertEqual(self.transaction_model.amount, new_transaction_amount)
        balance_after_transaction = account.balance
        transaction_amount_diff = round(
            Decimal(
                old_transaction_amount -
                new_transaction_amount),
            2)
        if self.transaction_model.sender_account == account:
            self.assertEqual(
                Decimal(
                    balance_before_transaction +
                    transaction_amount_diff),
                balance_after_transaction)
        elif self.transaction_model.receiver_account == account:
            self.assertEqual(
                Decimal(
                    balance_before_transaction -
                    transaction_amount_diff),
                balance_after_transaction)
        else:
            raise Exception("Account not used in transaction")

    def setUp(self) -> None:
        super().setUp()
        self.test_model: Transaction = Transaction.objects.get(id=4)
        self.user: User = User.objects.get(id=1)
        self.sender_account: PotAccount = PotAccount.objects.get(id=5)
        self.receiver_account: PotAccount = PotAccount.objects.get(id=6)
        self.sender_account2: PotAccount = PotAccount.objects.get(id=3)
        self.receiver_account2: PotAccount = PotAccount.objects.get(id=4)
        self.transaction_model: Transaction = Transaction()
        self.transaction_model.title = "New laptop"
        self.transaction_model.description = "Bought new laptop"
        self.transaction_model.amount = round(Decimal(2099.99), 2)
        self.transaction_model.currency = CurrencyType.GBP
        self.transaction_model.sender_account = self.sender_account
        self.transaction_model.receiver_account = self.receiver_account
        self.test_model: Transaction = Transaction.objects.get(id=4)
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

    def test_change_filename(self):
        self.transaction = Transaction.objects.get(id=2)
        self.assertFalse(
            change_filename(
                self.transaction, "test").find("transactions"), -1)

    def test_sender_account_balance_decreases_on_create_transaction(self):
        self._assert_balance_changes_on_transaction_created(
            self.sender_account)

    def test_receiver_account_balance_increases_on_create_transaction(self):
        self._assert_balance_changes_on_transaction_created(
            self.receiver_account)

    def test_sender_account_balance_increases_on_edit_transaction(self):
        self._assert_balance_changes_on_transaction_update(
            self.sender_account, round(Decimal(1800.00), 2))

    def test_sender_account_balance_decreases_on_edit_transaction(self):
        self._assert_balance_changes_on_transaction_update(
            self.sender_account, round(Decimal(2800.00), 2))

    def test_receiver_account_balance_increases_on_edit_transaction(self):
        self._assert_balance_changes_on_transaction_update(
            self.receiver_account, round(Decimal(1800.00), 2))

    def test_receiver_account_balance_decreases_on_edit_transaction(self):
        self._assert_balance_changes_on_transaction_update(
            self.receiver_account, round(Decimal(2800.00), 2))

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
        self.assertEqual(
            sender_account_balance_after_delete,
            sender_account_balance_before_delete +
            transaction_ammount)
        self.assertEqual(
            receiver_account_balance_after_delete,
            receiver_account_balance_before_delete -
            transaction_ammount)

    @freeze_time("2023-01-07 22:00:00")
    def test_valid_within_time_period(self):
        self.assertEqual(
            len(Transaction.get_transactions_from_time_period(Timespan.WEEK, self.user)), 8)

    @freeze_time("2023-01-07 22:00:00")
    def test_valid_split_categories(self):
        self.assertEqual(len(Transaction.get_category_splits(
            Transaction.get_transactions_from_time_period(Timespan.WEEK, self.user))), 2)

    @freeze_time("2023-01-07 22:00:00")
    def test_valid_split_categories_with_category_none(self):
        self._set_categories_none(self.transactions)
        self.assertEqual(len(Transaction.get_category_splits(
            Transaction.get_transactions_from_time_period(Timespan.WEEK, self.user))), 1)

    def test_account_balances_change_on_change_sender_account(self):
        self.transaction_model.save()

        self.sender_account.refresh_from_db()
        self.old_sender_account_balance_before = self.transaction_model.sender_account.balance
        self.new_sender_account_balance_before = self.sender_account2.balance
        self.transaction_model.sender_account = self.sender_account2
        self.transaction_model.save()
        self.transaction_model.refresh_from_db()
        self.sender_account.refresh_from_db()
        self.sender_account2.refresh_from_db()
        self.old_sender_account_balance_after = self.sender_account.balance
        self.new_sender_account_balance_after = self.sender_account2.balance
        self.assertEqual(
            self.old_sender_account_balance_before +
            self.transaction_model.amount,
            self.old_sender_account_balance_after)
        self.assertEqual(
            self.new_sender_account_balance_before -
            self.transaction_model.amount,
            self.new_sender_account_balance_after)

        self.receiver_account.refresh_from_db()
        self.old_receiver_account_balance_before = self.receiver_account.balance
        self.new_receiver_account_balance_before = self.receiver_account2.balance
        self.transaction_model.receiver_account = self.receiver_account2
        self.transaction_model.save()
        self.transaction_model.refresh_from_db()
        self.receiver_account.refresh_from_db()
        self.receiver_account2.refresh_from_db()
        self.old_receiver_account_balance_after = self.receiver_account.balance
        self.new_receiver_account_balance_after = self.receiver_account2.balance
        self.assertEqual(
            self.old_receiver_account_balance_before,
            self.old_receiver_account_balance_after +
            self.transaction_model.amount)
        self.assertEqual(
            self.new_receiver_account_balance_before,
            self.new_receiver_account_balance_after -
            self.transaction_model.amount)
