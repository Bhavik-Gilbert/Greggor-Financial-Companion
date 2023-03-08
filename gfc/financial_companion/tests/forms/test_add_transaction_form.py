from django import forms
from financial_companion.forms import AddTransactionForm
from financial_companion.models import Transaction, Category, Account, User
from .test_form_base import FormTestCase
from django.test import TestCase
from financial_companion.models import Transaction
# from financial_companion.tests.helpers.test_image import dragon.jpeg
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile


class AddTransactionFormTestCase(FormTestCase):
    """Test of the add transaction form"""

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        image_path = "financial_companion/tests/data/dragon.jpeg"
        # self.new_image = SimpleUploadedFile(name='dragon.jpeg', content=open(image_path, 'rb').read(), content_type='image/jpeg')
        self.form_input = {
            "title": "Test",
            "description": "This is a test transaction",
            "image": "transaction_reciept.jpeg",
            "category": 1,
            "amount": 152.95,
            "currency": "USD",
            "sender_account": 1,
            "receiver_account": 3,
        }

    def test_form_contains_required_fields(self):
        form = AddTransactionForm(self.user)
        self._assert_form_has_necessary_fields(
            form,
            'title',
            'description',
            'image',
            'category',
            'amount',
            'currency',
            'sender_account',
            'receiver_account'
        )

    def test_valid_add_transaction_form(self):
        form = AddTransactionForm(self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_title(self):
        self.form_input['title'] = ''
        form = AddTransactionForm(self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_30_character_title(self):
        self.form_input['title'] = '123456789012345678901234567890'
        form = AddTransactionForm(self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_over_30_character_title(self):
        self.form_input['title'] = '123456789012345678901234567890*'
        form = AddTransactionForm(self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_blank_description(self):
        self.form_input['description'] = ''
        form = AddTransactionForm(self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_accepts_blank_image(self):
        self.form_input['image'] = ''
        form = AddTransactionForm(self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_amount(self):
        self.form_input['amount'] = ''
        form = AddTransactionForm(self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_over_two_decimal_amount(self):
        self.form_input['amount'] = 1.999
        form = AddTransactionForm(self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_accepts_15_digit_amount(self):
        self.form_input['amount'] = '1234567891234.12'
        form = AddTransactionForm(self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_over_15_digit_amount(self):
        self.form_input['amount'] = '123456789123456.12'
        form = AddTransactionForm(self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_currency(self):
        self.form_input['currency'] = ''
        form = AddTransactionForm(self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = AddTransactionForm(self.user, data=self.form_input)
        before_count = Transaction.objects.count()
        transaction = form.save()
        after_count = Transaction.objects.count()
        self.assertEqual(after_count, before_count + 1)
        self.assertEqual(transaction.description, 'This is a test transaction')
        # self.assertEqual(transaction.image, self.new_image)
        self.assertTrue(isinstance(transaction.category, Category))
        self.assertEqual(transaction.category.id, 1)
        self.assertEqual(transaction.amount, Decimal("152.95"))
        self.assertEqual(transaction.currency, 'USD')
        self.assertTrue(isinstance(transaction.sender_account, Account))
        self.assertEqual(transaction.sender_account.id, 1)
        self.assertTrue(isinstance(transaction.receiver_account, Account))
        self.assertEqual(transaction.receiver_account.id, 3)

    def test_form_rejects_the_same_sender_and_receiver_accounts(self):
        self.form_input['receiver_account'] = 1
        form = AddTransactionForm(self.user, data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['receiver_account'][0],
            "The sender and receiver accounts cannot be the same.")

    def test_form_rejects_neither_the_sender_or_receiver_accounts_belonging_to_the_user(
            self):
        self.form_input['receiver_account'] = 2
        form = AddTransactionForm(self.user, data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertEquals(
            form.errors['receiver_account'][0],
            "Neither the sender or reciever are one of your accounts")
        self.assertEquals(
            form.errors['sender_account'][0],
            "Neither the sender or reciever are one of your accounts")
