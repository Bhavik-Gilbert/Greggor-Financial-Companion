from .test_view_base import ViewTestCase
from financial_companion.forms import AddRecurringTransactionForm
from financial_companion.models import RecurringTransaction, User
from django.urls import reverse
from decimal import Decimal


class EditTransactionViewTestCase(ViewTestCase):
    """Unit tests of the edit transaction view"""

    def setUp(self):
        self.url = reverse('edit_recurring_transaction', kwargs={"pk": 2})
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

    def test_edit_recurring_transaction_url(self):
        self.assertEqual(self.url, '/edit_recurring_transaction/2')

    def test_get_edit_recurring_transaction(self):
        self._login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'pages/add_recurring_transaction.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, AddRecurringTransactionForm))
        self.assertFalse(form.is_bound)

    def test_unsuccesfully_edit_recurring_transaction(self):
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
        # self.assertTrue(form.is_bound)
        transaction = RecurringTransaction.objects.get(id=2)
        transaction.refresh_from_db()
        self.assertEqual(
            transaction.description,
            "Paying off hire car.")
        # self.assertEqual(transaction.image, "transaction_reciept.jpeg")
        self.assertEqual(transaction.category.id, 1)
        self.assertEqual(transaction.amount, Decimal("130.59"))
        self.assertEqual(transaction.currency, 'USD')
        self.assertEqual(transaction.sender_account.id, 3)
        self.assertEqual(transaction.receiver_account.id, 4)

    def test_succesfully_edit_recurring_transaction(self):
        self._login(self.user)
        before_count = RecurringTransaction.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = RecurringTransaction.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('view_recurring_transactions')
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(
            response, 'pages/view_recurring_transactions.html')
        transaction = RecurringTransaction.objects.get(id=2)
        transaction.refresh_from_db()
        self.assertEqual(transaction.title, "Test")
        self.assertEqual(transaction.description, "This is a test transaction")
        # self.assertEqual(transaction.image, "transaction_reciept.jpeg")
        self.assertEqual(transaction.category.id, 1)
        self.assertEqual(transaction.amount, Decimal("152.95"))
        self.assertEqual(transaction.currency, 'USD')
        self.assertEqual(transaction.sender_account.id, 1)
        self.assertEqual(transaction.receiver_account.id, 3)

    def test_invalid_recurring_transaction_id_given(self):
        self._login(self.user)
        invalid_url = reverse(
            'edit_recurring_transaction', kwargs={
                'pk': 100000})
        response = self.client.get(invalid_url, follow=True)
        response_url = reverse('view_recurring_transactions')
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(
            response, 'pages/view_recurring_transactions.html')

    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
