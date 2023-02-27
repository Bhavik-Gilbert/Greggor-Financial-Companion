from .test_view_base import ViewTestCase
from financial_companion.forms import AddTransactionForm
from financial_companion.models import Transaction, User
from django.urls import reverse


class DeleteTransactionViewTestCase(ViewTestCase):
    """Unit tests of the delete transaction view"""

    def setUp(self):
        self.url = reverse('delete_transaction', kwargs={"pk": 2})
        self.user = User.objects.get(username='@johndoe')

    def test_delete_transaction_url(self):
        self.assertEqual(self.url, '/delete_transaction/2')

    def test_get_delete_transaction(self):
        self._login(self.user)
        transaction = Transaction.objects.get(id=2)
        before_count = Transaction.objects.count()
        response = self.client.get(self.url)
        after_count = Transaction.objects.count()
        self.assertEqual(before_count - 1, after_count)
        response_url = reverse('view_transactions', kwargs={'filter_type': "all"})
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)

    def test_transaction_does_not_exist(self):
        self._login(self.user)
        self.url = reverse('delete_transaction', kwargs={'pk': 1000})
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
