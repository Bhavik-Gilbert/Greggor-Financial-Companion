from .test_view_base import ViewTestCase
from financial_companion.forms import AddTransactionsViaBankStatementForm
from financial_companion.models import Transaction, User, PotAccount
from financial_companion.helpers import CurrencyType
from django.urls import reverse
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models import Q
import os
from django.contrib.messages import get_messages
from typing import Any


class AddTransactionsViaBankStatementViewTestCase(ViewTestCase):
    """Unit tests of the add transactions via bank statement view"""

    def setUp(self):
        self.url = reverse('add_transactions_via_bank_statement')
        self.user: User = User.objects.get(username="@johndoe")
        self.account: PotAccount = PotAccount.objects.filter(
            user=self.user).first()
        bank_statement_path: str = os.path.join(
            "financial_companion", "tests", "data", "bank_statement.pdf")
        uploaded_bank_statement: TemporaryUploadedFile = self._get_upload_file(
            bank_statement_path)

        self.form_input: dict[str, Any] = {
            "bank_statement": uploaded_bank_statement,
            "account_currency": CurrencyType.GBP,
            "update_balance": "False",
            "account": self.account.id
        }

    def test_valid_add_transaction_via_bank_statement_url(self):
        self.assertEqual(self.url, '/add_transactions_via_bank_statement/')

    def test_valid_get_add_transaction_via_bank_statement(self):
        self._login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'pages/add_transactions_via_bank_statement_form.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, AddTransactionsViaBankStatementForm))
        self.assertFalse(form.is_bound)

    def test_valid_unsuccesfully_add_transaction_via_bank_statement(self):
        self._login(self.user)
        self.form_input.pop('bank_statement')
        before_count = Transaction.objects.filter(
            Q(sender_account=self.account) | Q(receiver_account=self.account)).count()
        response = self.client.post(self.url, self.form_input)
        after_count = Transaction.objects.filter(
            Q(sender_account=self.account) | Q(receiver_account=self.account)).count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'pages/add_transactions_via_bank_statement_form.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, AddTransactionsViaBankStatementForm))
        self.assertTrue(form.is_bound)

    def test_valid_succesfully_add_transaction_via_bank_statement(self):
        self._login(self.user)
        before_count = Transaction.objects.filter(
            Q(sender_account=self.account) | Q(receiver_account=self.account)).count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Transaction.objects.filter(
            Q(sender_account=self.account) | Q(receiver_account=self.account)).count()
        self.assertEqual(after_count, before_count + 33)
        response_url = reverse(
            'view_transactions_redirect')
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, 'pages/display_transactions.html')
        messages_list: list[Any] = list(get_messages(response.wsgi_request))
        self.assertTrue(any(
            'new transactions added' in message.message for message in messages_list))

    def test_invalid_succesfully_add_transaction_via_bank_statement_invalid_pdf(
            self):
        bank_statement_path: str = os.path.join(
            "financial_companion", "tests", "data", "invalid_bank_statement.pdf")
        uploaded_bank_statement: TemporaryUploadedFile = self._get_upload_file(
            bank_statement_path)
        self.form_input["bank_statement"] = uploaded_bank_statement
        self._login(self.user)
        before_count = Transaction.objects.filter(
            Q(sender_account=self.account) | Q(receiver_account=self.account)).count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Transaction.objects.filter(
            Q(sender_account=self.account) | Q(receiver_account=self.account)).count()
        self.assertEqual(after_count, before_count)
        response_url = self.url
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'pages/add_transactions_via_bank_statement_form.html')
        messages_list: list[Any] = list(get_messages(response.wsgi_request))
        self.assertTrue(any(
            'Error scanning document, please ensure it is a valid bank statement' == message.message for message in messages_list))

    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
