from financial_companion.forms import AddRecurringTransactionForm
from financial_companion.models import RecurringTransaction, Category, Account, User
from .test_form_base import FormTestCase
from decimal import Decimal
from typing import Any


class AddRecurringTransactionFormTestCase(FormTestCase):
    """Unit tests of the add recurring transaction form"""

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
            "start_date": "2023-01-31",
            "end_date": "2023-05-22",
            "interval": "month",
        }

    def test_form_contains_required_fields(self):
        form: AddRecurringTransactionForm = AddRecurringTransactionForm(
            self.user)
        self._assert_form_has_necessary_fields(
            form,
            'title',
            'description',
            'file',
            'category',
            'amount',
            'currency',
            'sender_account',
            'receiver_account',
            'start_date',
            'end_date',
            'interval',
        )

    def test_valid_add_recurring_transaction_form(self):
        form: AddRecurringTransactionForm = AddRecurringTransactionForm(
            self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_title(self):
        self.form_input['title']: str = ''
        form: AddRecurringTransactionForm = AddRecurringTransactionForm(
            self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_30_character_title(self):
        self.form_input['title']: str = '123456789012345678901234567890'
        form: AddRecurringTransactionForm = AddRecurringTransactionForm(
            self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_over_30_character_title(self):
        self.form_input['title']: str = '123456789012345678901234567890*'
        form: AddRecurringTransactionForm = AddRecurringTransactionForm(
            self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_interval(self):
        self.form_input['interval']: str = ''
        form: AddRecurringTransactionForm = AddRecurringTransactionForm(
            self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_blank_description(self):
        self.form_input['description']: str = ''
        form: AddRecurringTransactionForm = AddRecurringTransactionForm(
            self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_blank_file(self):
        self.form_input['file']: str = ''
        form: AddRecurringTransactionForm = AddRecurringTransactionForm(
            self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_amount(self):
        self.form_input['amount']: str = ''
        form: AddRecurringTransactionForm = AddRecurringTransactionForm(
            self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_over_two_decimal_amount(self):
        self.form_input['amount']: Decimal = 1.999
        form: AddRecurringTransactionForm = AddRecurringTransactionForm(
            self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_15_digit_amount(self):
        self.form_input['amount']: str = '1234567891234.12'
        form: AddRecurringTransactionForm = AddRecurringTransactionForm(
            self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_over_15_digit_amount(self):
        self.form_input['amount']: str = '123456789123456.12'
        form: AddRecurringTransactionForm = AddRecurringTransactionForm(
            self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_currency(self):
        self.form_input['currency']: str = ''
        form: AddRecurringTransactionForm = AddRecurringTransactionForm(
            self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_end_date_after_start_valid(self):
        self.form_input['end_date']: str = '2023-06-29'
        form: AddRecurringTransactionForm = AddRecurringTransactionForm(
            self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_start_date_after_end_invalid(self):
        self.form_input['end_date']: str = '2023-01-01'
        form: AddRecurringTransactionForm = AddRecurringTransactionForm(
            self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_the_same_sender_and_receiver_accounts(self):
        self.form_input['receiver_account']: int = 1
        self.form_input['sender_account']: int = 1
        form: AddRecurringTransactionForm = AddRecurringTransactionForm(
            self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_neither_the_sender_or_receiver_accounts_belonging_to_the_user(
            self):
        self.form_input['receiver_account']: int = 2
        form: AddRecurringTransactionForm = AddRecurringTransactionForm(
            self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form: AddRecurringTransactionForm = AddRecurringTransactionForm(
            self.user, data=self.form_input)
        before_count: int = RecurringTransaction.objects.count()
        transaction: RecurringTransaction = form.save()
        after_count: int = RecurringTransaction.objects.count()
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

    def test_form_must_save_via_edit_correctly(self):
        before_count: int = RecurringTransaction.objects.count()
        old_transaction: RecurringTransaction = RecurringTransaction.objects.get(
            id=2)
        form: AddRecurringTransactionForm = AddRecurringTransactionForm(
            self.user, data=self.form_input, instance=old_transaction)
        new_rec_transaction: RecurringTransaction = form.save(
            instance=old_transaction)
        after_count: int = RecurringTransaction.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(
            new_rec_transaction.description,
            'This is a test transaction')
        self.assertTrue(isinstance(new_rec_transaction.category, Category))
        self.assertEqual(new_rec_transaction.category.id, 1)
        self.assertEqual(new_rec_transaction.amount, Decimal("152.95"))
        self.assertEqual(new_rec_transaction.currency, 'USD')
        self.assertTrue(
            isinstance(
                new_rec_transaction.sender_account,
                Account))
        self.assertEqual(new_rec_transaction.sender_account.id, 1)
        self.assertTrue(
            isinstance(
                new_rec_transaction.receiver_account,
                Account))
        self.assertEqual(new_rec_transaction.receiver_account.id, 3)
