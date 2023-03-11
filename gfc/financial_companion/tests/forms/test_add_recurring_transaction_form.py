from django import forms
from financial_companion.forms import AddRecurringTransactionForm
from financial_companion.models import RecurringTransaction, Transaction, Category, Account, User
from .test_form_base import FormTestCase
from django.test import TestCase
from financial_companion.models import Transaction
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile


class AddRecurringTransactionFormTestCase(FormTestCase):
    """Test of the add transaction form"""

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        image_path = "financial_companion/tests/data/dragon.jpeg"
        self.form_input = {
            "title": "Test",
            "description": "This is a test transaction",
            "image": "transaction_reciept.jpeg",
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
        form = AddRecurringTransactionForm(self.user)
        self._assert_form_has_necessary_fields(
            form,
            'title',
            'description',
            'image',
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
        form = AddRecurringTransactionForm(self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_title(self):
        self.form_input['title'] = ''
        form = AddRecurringTransactionForm(self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_30_character_title(self):
        self.form_input['title'] = '123456789012345678901234567890'
        form = AddRecurringTransactionForm(self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_over_30_character_title(self):
        self.form_input['title'] = '123456789012345678901234567890*'
        form = AddRecurringTransactionForm(self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_interval(self):
        self.form_input['interval'] = ''
        form = AddRecurringTransactionForm(self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_blank_description(self):
        self.form_input['description'] = ''
        form = AddRecurringTransactionForm(self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_blank_image(self):
        self.form_input['image'] = ''
        form = AddRecurringTransactionForm(self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_amount(self):
        self.form_input['amount'] = ''
        form = AddRecurringTransactionForm(self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_over_two_decimal_amount(self):
        self.form_input['amount'] = 1.999
        form = AddRecurringTransactionForm(self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_15_digit_amount(self):
        self.form_input['amount'] = '1234567891234.12'
        form = AddRecurringTransactionForm(self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_over_15_digit_amount(self):
        self.form_input['amount'] = '123456789123456.12'
        form = AddRecurringTransactionForm(self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_currency(self):
        self.form_input['currency'] = ''
        form = AddRecurringTransactionForm(self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_end_date_after_start_valid(self):
        self.form_input['end_date'] = '2023-06-29'
        form = AddRecurringTransactionForm(self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_start_date_after_end_invalid(self):
        self.form_input['end_date'] = '2023-01-01'
        form = AddRecurringTransactionForm(self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_the_same_sender_and_receiver_accounts(self):
        self.form_input['receiver_account'] = 1
        self.form_input['sender_account'] = 1
        form = AddRecurringTransactionForm(self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_neither_the_sender_or_receiver_accounts_belonging_to_the_user(
            self):
        self.form_input['receiver_account'] = 2
        form = AddRecurringTransactionForm(self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = AddRecurringTransactionForm(self.user, data=self.form_input)
        before_count = RecurringTransaction.objects.count()
        transaction = form.save()
        after_count = RecurringTransaction.objects.count()
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
        old_transaction = RecurringTransaction.objects.get(id=2)
        form = AddRecurringTransactionForm(self.user, data=self.form_input)
        new_rec_transaction = form.save(old_transaction)
        before_count = RecurringTransaction.objects.count()
        after_count = RecurringTransaction.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(
            new_rec_transaction.description,
            'This is a test transaction')
        # self.assertEqual(transaction.image, self.new_image)
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
