from .test_view_base import ViewTestCase
from financial_companion.forms import AddRecurringTransactionForm
from financial_companion.models import RecurringTransaction, User
from django.urls import reverse
from decimal import Decimal
from django.http import HttpResponse


class EditRecurringTransactionViewTestCase(ViewTestCase):
    """Unit tests of the edit recurring transaction view"""

    def setUp(self) -> None:
        self.url: str = reverse('edit_recurring_transaction', kwargs={"pk": 2})
        self.image_path: str = "financial_companion/tests/data/dragon.jpeg"
        self.image_upload = self._get_image_upload_file(
            self.image_path, "jpeg")
        self.form_input = {
            "title": "Test",
            "description": "This is a test transaction",
            "file": self.image_upload,
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

    def test_edit_recurring_transaction_url(self) -> None:
        self.assertEqual(self.url, '/edit_recurring_transaction/2')

    def test_get_edit_recurring_transaction(self) -> None:
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'pages/add_recurring_transaction.html')
        form: AddRecurringTransactionForm = response.context['form']
        self.assertTrue(isinstance(form, AddRecurringTransactionForm))
        self.assertFalse(form.is_bound)

    def test_unsuccesfully_edit_recurring_transaction(self) -> None:
        self._login(self.user)
        self.form_input['title']: str = ''
        before_count: int = RecurringTransaction.objects.count()
        response: HttpResponse = self.client.post(self.url, self.form_input)
        after_count: int = RecurringTransaction.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'pages/add_recurring_transaction.html')
        form: AddRecurringTransactionForm = response.context['form']
        self.assertTrue(isinstance(form, AddRecurringTransactionForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(form.is_valid())
        transaction: RecurringTransaction = RecurringTransaction.objects.get(
            id=2)
        transaction.refresh_from_db()
        self.assertEqual(
            transaction.description,
            "Paying off hire car.")
        self.assertFalse("transactions/" in transaction.file.name)
        self.assertFalse(self.image_path.split(
            "/")[-1].split(".")[-1] in transaction.file.name)
        self.assertEqual(transaction.category.id, 1)
        self.assertEqual(transaction.amount, Decimal("130.59"))
        self.assertEqual(transaction.currency, 'USD')
        self.assertEqual(transaction.sender_account.id, 3)
        self.assertEqual(transaction.receiver_account.id, 4)

    def test_succesfully_edit_recurring_transaction(self) -> None:
        self._login(self.user)
        before_count: int = RecurringTransaction.objects.count()
        response: HttpResponse = self.client.post(
            self.url, self.form_input, follow=True)
        after_count: int = RecurringTransaction.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse(
            'individual_recurring_transaction',
            kwargs={
                'pk': 2})
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(
            response, 'pages/individual_recurring_transaction.html')
        recurring_transaction: RecurringTransaction = RecurringTransaction.objects.get(
            id=2)
        recurring_transaction.refresh_from_db()
        self.assertEqual(recurring_transaction.title, "Test")
        self.assertEqual(
            recurring_transaction.description,
            "This is a test transaction")
        self.assertTrue("transactions/" in recurring_transaction.file.name)
        self.assertTrue(self.image_path.split(
            "/")[-1].split(".")[-1] in recurring_transaction.file.name)
        self.assertEqual(recurring_transaction.category.id, 1)
        self.assertEqual(recurring_transaction.amount, Decimal("152.95"))
        self.assertEqual(recurring_transaction.currency, 'USD')
        self.assertEqual(recurring_transaction.sender_account.id, 1)
        self.assertEqual(recurring_transaction.receiver_account.id, 3)

    def test_invalid_recurring_transaction_id_given(self) -> None:
        self._login(self.user)
        invalid_url = reverse(
            'edit_recurring_transaction', kwargs={
                'pk': 100000})
        response: HttpResponse = self.client.get(invalid_url, follow=True)
        response_url = reverse('view_recurring_transactions')
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(
            response, 'pages/view_recurring_transactions.html')

    def test_get_view_redirects_when_not_logged_in(self) -> None:
        self._assert_require_login(self.url)
