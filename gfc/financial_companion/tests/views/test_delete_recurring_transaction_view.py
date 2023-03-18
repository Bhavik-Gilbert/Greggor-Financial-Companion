from .test_view_base import ViewTestCase
from financial_companion.forms import AddRecurringTransactionForm
from financial_companion.models import RecurringTransaction, User, Transaction
from django.urls import reverse
from django.http import HttpRequest, HttpResponse


class DeleteRecurringTransactionViewTestCase(ViewTestCase):
    """Unit tests of the delete recurring transaction view"""

    def setUp(self) -> None:
        self.url: str = reverse(
            'delete_recurring_transaction',
            kwargs={
                "pk": 2})
        self.user: User = User.objects.get(username='@johndoe')

    def test_delete_recurring_transaction_url(self) -> None:
        self.assertEqual(self.url, '/delete_recurring_transaction/2')

    def test_get_delete_recurring_transaction(self) -> None:
        self._login(self.user)
        recurring_transaction: RecurringTransaction = RecurringTransaction.objects.get(
            id=2)
        before_count: int = RecurringTransaction.objects.count()
        response: HttpResponse = self.client.get(self.url)
        after_count: int = RecurringTransaction.objects.count()
        self.assertEqual(before_count - 1, after_count)
        response_url: str = reverse('dashboard')
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)

    def test_recurring_transaction_does_not_exist(self) -> None:
        self._login(self.user)
        self.url: str = reverse(
            'delete_recurring_transaction',
            kwargs={
                'pk': 1000})
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

    def test_delete_recurring_transaction_keeps_associated_transactions(
            self) -> None:
        self._login(self.user)
        recurring_transaction: RecurringTransaction = RecurringTransaction.objects.get(
            id=2)
        before_rec_count: int = RecurringTransaction.objects.count()
        before_count: int = Transaction.objects.count()
        response: HttpResponse = self.client.get(self.url)
        after_rec_count: int = RecurringTransaction.objects.count()
        after_count: int = Transaction.objects.count()
        self.assertEqual(before_rec_count - 1, after_rec_count)
        self.assertEqual(before_count, after_count)
        response_url: str = reverse('dashboard')
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
