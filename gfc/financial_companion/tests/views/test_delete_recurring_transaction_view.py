from .test_view_base import ViewTestCase
from financial_companion.forms import AddRecurringTransactionForm
from financial_companion.models import RecurringTransaction, User, Transaction
from django.urls import reverse


class DeleteTransactionViewTestCase(ViewTestCase):
    """Unit tests of the delete transaction view"""

    def setUp(self):
        self.url = reverse('delete_recurring_transaction', kwargs={"pk": 2})
        self.user = User.objects.get(username='@johndoe')

    def test_delete_transaction_url(self):
        self.assertEqual(self.url, '/delete_recurring_transaction/2')

    def test_get_delete_transaction(self):
        self._login(self.user)
        transaction = RecurringTransaction.objects.get(id=2)
        before_count = RecurringTransaction.objects.count()
        response = self.client.get(self.url)
        after_count = RecurringTransaction.objects.count()
        self.assertEqual(before_count - 1, after_count)
        response_url = reverse('dashboard')
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)

    def test_transaction_does_not_exist(self):
        self._login(self.user)
        self.url = reverse('delete_recurring_transaction', kwargs={'pk': 1000})
        before_count = User.objects.count()
        response = self.client.get(self.url)
        after_count = User.objects.count()
        self.assertEqual(before_count, after_count)
        response_url = reverse('dashboard')
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)

    def test_delete_recurring_transaction_keeps_associated_transactions(self):
        self._login(self.user)
        transaction = RecurringTransaction.objects.get(id=2)
        before_rec_count = RecurringTransaction.objects.count()
        before_count = Transaction.objects.count()
        response = self.client.get(self.url)
        after_rec_count = RecurringTransaction.objects.count()
        after_count = Transaction.objects.count()
        self.assertEqual(before_rec_count - 1, after_rec_count)
        self.assertEqual(before_count, after_count)
        response_url = reverse('dashboard')
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
