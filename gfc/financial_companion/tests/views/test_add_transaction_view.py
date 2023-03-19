from .test_view_base import ViewTestCase
from financial_companion.forms import AddTransactionForm
from financial_companion.models import Transaction, User
from django.urls import reverse
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from typing import Any


class AddTransactionViewTestCase(ViewTestCase):
    """Unit tests of the add transaction view"""

    def setUp(self) -> None:
        self.url = reverse('add_transaction')
        self.image_path: str = "financial_companion/tests/data/dragon.jpeg"
        self.image_upload: SimpleUploadedFile = self._get_image_upload_file(
            self.image_path, "jpeg")
        self.form_input: dict[str, Any] = {
            "title": "Test",
            "description": "This is a test transaction",
            "image": self.image_upload,
            "category": 1,
            "amount": 152.95,
            "currency": "USD",
            "sender_account": 1,
            "receiver_account": 3,
        }
        self.user: User = User.objects.get(username='@johndoe')

    def test_add_transaction_url(self) -> None:
        self.assertEqual(self.url, '/add_transaction/')

    def test_get_add_transaction(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/add_transaction.html')
        form: AddTransactionForm = response.context['form']
        self.assertTrue(isinstance(form, AddTransactionForm))
        self.assertFalse(form.is_bound)

    def test_unsuccesfully_add_transaction(self) -> Any:
        self._login(self.user)
        self.form_input['title']: str = ''
        before_count: int = Transaction.objects.count()
        response: HttpResponse = self.client.post(self.url, self.form_input)
        after_count: int = Transaction.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/add_transaction.html')
        form: AddTransactionForm = response.context['form']
        self.assertTrue(isinstance(form, AddTransactionForm))
        self.assertTrue(form.is_bound)

    def test_succesfully_add_transaction(self) -> None:
        self._login(self.user)
        before_count: int = Transaction.objects.count()
        response: HttpResponse = self.client.post(
            self.url, self.form_input, follow=True)
        after_count: int = Transaction.objects.count()
        self.assertEqual(after_count, before_count + 1)
        response_url: str = reverse(
            'view_transactions', kwargs={
                'filter_type': "all"})
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, 'pages/display_transactions.html')
        transaction: Transaction = Transaction.objects.get(title='Test')
        self.assertEqual(transaction.description, 'This is a test transaction')
        self.assertTrue("transactions/" in transaction.image.name)
        self.assertTrue(self.image_path.split(
            "/")[-1].split(".")[-1] in transaction.image.name)
        self.assertEqual(transaction.category.id, 1)
        self.assertEqual(transaction.amount, Decimal("152.95"))
        self.assertEqual(transaction.currency, 'USD')
        self.assertEqual(transaction.sender_account.id, 1)
        self.assertEqual(transaction.receiver_account.id, 3)

    def test_get_view_redirects_when_not_logged_in(self) -> None:
        self._assert_require_login(self.url)
