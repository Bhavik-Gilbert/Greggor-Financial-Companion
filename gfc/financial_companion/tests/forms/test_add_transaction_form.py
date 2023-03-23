from financial_companion.forms import AddTransactionForm
from financial_companion.models import Transaction, Category, Account, User
from .test_form_base import FormTestCase
from financial_companion.models import Transaction
from decimal import Decimal
from typing import Any


class AddTransactionFormTestCase(FormTestCase):
    """Unit tests of the add transaction form"""

    def setUp(self):
        super().setUp()
        self.user: User = User.objects.get(username='@johndoe')
        self.form_input: dict[str, Any] = {
            "title": "Test",
            "description": "This is a test transaction",
            "file": "transaction_reciept.jpeg",
            "category": 1,
            "amount": 152.95,
            "currency": "USD",
            "sender_account": 1,
            "receiver_account": 3,
        }

    def test_form_contains_required_fields(self):
        form: AddTransactionForm = AddTransactionForm(self.user)
        self._assert_form_has_necessary_fields(
            form,
            'title',
            'description',
            'file',
            'category',
            'amount',
            'currency',
            'sender_account',
            'receiver_account'
        )

    def test_valid_add_transaction_form(self):
        form: AddTransactionForm = AddTransactionForm(
            self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_title(self):
        self.form_input['title']: str = ''
        form: AddTransactionForm = AddTransactionForm(
            self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_30_character_title(self):
        self.form_input['title']: str = '123456789012345678901234567890'
        form: AddTransactionForm = AddTransactionForm(
            self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_over_30_character_title(self):
        self.form_input['title']: str = '123456789012345678901234567890*'
        form: AddTransactionForm = AddTransactionForm(
            self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_blank_description(self):
        self.form_input['description']: str = ''
        form: AddTransactionForm = AddTransactionForm(
            self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_blank_file(self):
        self.form_input['file']: str = ''
        form: AddTransactionForm = AddTransactionForm(
            self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_amount(self):
        self.form_input['amount']: str = ''
        form: AddTransactionForm = AddTransactionForm(
            self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_over_two_decimal_amount(self):
        self.form_input['amount']: Decimal = 1.999
        form: AddTransactionForm = AddTransactionForm(
            self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_15_digit_amount(self):
        self.form_input['amount']: str = '1234567891234.12'
        form: AddTransactionForm = AddTransactionForm(
            self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_over_15_digit_amount(self):
        self.form_input['amount']: str = '123456789123456.12'
        form: AddTransactionForm = AddTransactionForm(
            self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_currency(self):
        self.form_input['currency']: str = ''
        form: AddTransactionForm = AddTransactionForm(
            self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form: AddTransactionForm = AddTransactionForm(
            self.user, data=self.form_input)
        before_count: int = Transaction.objects.count()
        transaction: Transaction = form.save()
        after_count: int = Transaction.objects.count()
        self.assertEqual(after_count, before_count + 1)
        self.assertEqual(transaction.description, 'This is a test transaction')
        self.assertTrue(isinstance(transaction.category, Category))
        self.assertEqual(transaction.category.id, 1)
        self.assertEqual(transaction.amount, Decimal("152.95"))
        self.assertEqual(transaction.currency, 'USD')
        self.assertTrue(isinstance(transaction.sender_account, Account))
        self.assertEqual(transaction.sender_account.id, 1)
        self.assertTrue(isinstance(transaction.receiver_account, Account))
        self.assertEqual(transaction.receiver_account.id, 3)

    def test_form_rejects_the_same_sender_and_receiver_accounts(self):
        self.form_input['receiver_account']: int = 1
        form: AddTransactionForm = AddTransactionForm(
            self.user, data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['receiver_account'][0],
            "The sender and receiver accounts cannot be the same.")

    def test_form_must_save_via_edit_correctly(self):
        old_transaction: Transaction = Transaction.objects.get(id=2)
        form: AddTransactionForm = AddTransactionForm(
            self.user, data=self.form_input, instance=old_transaction)
        before_count: int = Transaction.objects.count()
        new_transaction: Transaction = form.save(instance=old_transaction)
        after_count: int = Transaction.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(
            new_transaction.description,
            'This is a test transaction')
        self.assertTrue(isinstance(new_transaction.category, Category))
        self.assertEqual(new_transaction.category.id, 1)
        self.assertEqual(new_transaction.amount, Decimal("152.95"))
        self.assertEqual(new_transaction.currency, 'USD')
        self.assertTrue(isinstance(new_transaction.sender_account, Account))
        self.assertEqual(new_transaction.sender_account.id, 1)
        self.assertTrue(isinstance(new_transaction.receiver_account, Account))
        self.assertEqual(new_transaction.receiver_account.id, 3)

    def test_form_rejects_neither_the_sender_or_receiver_accounts_belonging_to_the_user(
            self):
        self.form_input['receiver_account']: int = 2
        form: AddTransactionForm = AddTransactionForm(
            self.user, data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEquals(
            form.errors['receiver_account'][0],
            "Neither the sender or reciever are accounts with a balance to track.")
        self.assertEquals(
            form.errors['sender_account'][0],
            "Neither the sender or reciever are accounts with a balance to track.")
