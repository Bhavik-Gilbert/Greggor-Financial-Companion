from .test_view_base import ViewTestCase
from financial_companion.forms import AddRecurringTransactionForm
from financial_companion.models import RecurringTransaction, Transaction, User
from django.urls import reverse
from decimal import Decimal


class AddRecurringTransactionViewTestCase(ViewTestCase):
    """Unit tests of the add recurring transaction view"""

    def setUp(self):
        self.url = reverse('add_recurring_transaction')
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
        self.user = User.objects.get(username='@johndoe')

    def test_add_recurring_transaction_url(self):
        self.assertEqual(self.url, '/add_recurring_transaction/')

    def test_get_add_recurring_transaction(self):
        self._login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'pages/add_recurring_transaction.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, AddRecurringTransactionForm))
        self.assertFalse(form.is_bound)

    def test_unsuccesfully_add_recurring_transaction(self):
        self._login(self.user)
        self.form_input['title'] = ''
        before_count = RecurringTransaction.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = RecurringTransaction.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'pages/add_recurring_transaction.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, AddRecurringTransactionForm))
        self.assertTrue(form.is_bound)

    def test_succesfully_add_recurring_transaction(self):
        self._login(self.user)
        before_count = RecurringTransaction.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = RecurringTransaction.objects.count()
        self.assertEqual(after_count, before_count + 1)
        response_url = reverse('view_recurring_transactions')
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(
            response, 'pages/view_recurring_transactions.html')
        transaction = RecurringTransaction.objects.get(title='Test')
        self.assertEqual(transaction.description, 'This is a test transaction')
        self.assertEqual(transaction.category.id, 1)
        self.assertEqual(transaction.amount, Decimal("152.95"))
        self.assertEqual(transaction.currency, 'USD')
        self.assertEqual(transaction.sender_account.id, 1)
        self.assertEqual(transaction.receiver_account.id, 3)

    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
