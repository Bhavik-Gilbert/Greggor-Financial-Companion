from .test_view_base import ViewTestCase
from financial_companion.models import Transaction, User
from django.urls import reverse
from django.http import HttpResponse


class DeleteTransactionViewTestCase(ViewTestCase):
    """Unit tests of the delete transaction view"""

    def setUp(self) -> None:
        self.url: str = reverse('delete_transaction', kwargs={"pk": 2})
        self.user: User = User.objects.get(username='@johndoe')

    def test_delete_transaction_url(self) -> None:
        self.assertEqual(self.url, '/delete_transaction/2')

    def test_get_delete_transaction(self) -> None:
        self._login(self.user)
        transaction: Transaction = Transaction.objects.get(id=2)
        before_count: int = Transaction.objects.count()
        response: HttpResponse = self.client.get(self.url)
        after_count: int = Transaction.objects.count()
        self.assertEqual(before_count - 1, after_count)
        response_url: str = reverse(
            'view_transactions', kwargs={
                'filter_type': "all"})
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)

    def test_transaction_does_not_exist(self) -> None:
        self._login(self.user)
        self.url: str = reverse('delete_transaction', kwargs={'pk': 1000})
        before_count: int = User.objects.count()
        response: HttpResponse = self.client.get(self.url)
        after_count: int = User.objects.count()
        self.assertEqual(before_count, after_count)
        response_url: str = reverse('dashboard')
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
