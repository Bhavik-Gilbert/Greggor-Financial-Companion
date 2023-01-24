from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from typing import Any

from .test_view_base import ViewTestCase
from financial_companion.forms import PotAccountForm, BankAccountForm
from financial_companion.models import User, PotAccount, BankAccount
from financial_companion.helpers import MonetaryAccountType, CurrencyType
from decimal import Decimal

class AddMonetaryAccountViewTestCase(ViewTestCase):
    """Unit tests of the add monetary account view"""

    def setUp(self):
        self.user: User = User.objects.get(username="@johndoe")
        self.url: str = reverse(f"add_monetary_account")


    def test_valid_page_url(self):
        self.assertEqual(self.url,'/add_monetary_account/')

    def test_valid_get_page(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/monetary_accounts_form.html')
        form: PotAccountForm = response.context['form']
        self.assertTrue(isinstance(form, PotAccountForm))
        form_toggle: bool = response.context['form_toggle']
        self.assertTrue(form_toggle)
        account_type: MonetaryAccountType = response.context['account_type']
        self.assertEqual(account_type, MonetaryAccountType.POT)
        monetary_account_types: MonetaryAccountType = response.context['monetary_account_types']
        self.assertEqual(monetary_account_types, MonetaryAccountType)
        self.assertFalse(form.is_bound)
    
    def test_valid_post_account_type_pot(self):
        self._login(self.user)
        form_input: dict[str, Any] = {'account_type': MonetaryAccountType.POT}
        response: HttpResponse = self.client.post(self.url, form_input)
        account_type: MonetaryAccountType = response.context['account_type']
        self.assertEqual(account_type, MonetaryAccountType.POT)
        form: PotAccountForm = response.context['form']
        self.assertTrue(isinstance(form, PotAccountForm))
    
    def test_valid_post_account_type_bank(self):
        self._login(self.user)
        form_input: dict[str, Any] = {'account_type': MonetaryAccountType.BANK}
        response: HttpResponse = self.client.post(self.url, form_input)
        account_type: MonetaryAccountType = response.context['account_type']
        self.assertEqual(account_type, MonetaryAccountType.BANK)
        form: PotAccountForm = response.context['form']
        self.assertTrue(isinstance(form, BankAccountForm))
    
    def test_valid_pot_account_form_input(self):
        self._login(self.user)
        pot_account_count_before: int = PotAccount.objects.count()
        bank_account_count_before: int = BankAccount.objects.count()
        form_input: dict[str, Any]= {
            "name": "Test Pot",
            "description": "This is a test pot",
            "balance": Decimal("99.99"),
            "currency": CurrencyType.GBP,
            "submit_type": MonetaryAccountType.POT
        }
        response: HttpResponse = self.client.post(self.url, form_input, follow=True)
        response_url: str = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'pages/dashboard.html')
        pot_account_count_after: int = PotAccount.objects.count()
        bank_account_count_after: int = BankAccount.objects.count()
        self.assertEqual(pot_account_count_before + 1, pot_account_count_after)
        self.assertEqual(bank_account_count_before, bank_account_count_after)
    
    def test_valid_bank_account_form_input(self):
        self._login(self.user)
        pot_account_count_before: int = PotAccount.objects.count()
        bank_account_count_before: int = BankAccount.objects.count()
        form_input: dict[str, Any] = {
            "name": "Test Bank",
            "description": "This is a test bank",
            "balance": Decimal("99.99"),
            "currency": CurrencyType.GBP,
            "bank_name": "Best Test Bank",
            "account_number": "12345678",
            "sort_code": "123456",
            "iban": "GB1234567890112345",
            "interest_rate": 0,
            "submit_type": MonetaryAccountType.BANK
        }
        response: HttpResponse = self.client.post(self.url, form_input, follow=True)
        response_url: str = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'pages/dashboard.html')
        pot_account_count_after: int = PotAccount.objects.count()
        bank_account_count_after: int = BankAccount.objects.count()
        self.assertEqual(pot_account_count_before + 1, pot_account_count_after)
        self.assertEqual(bank_account_count_before + 1, bank_account_count_after)
    
    def test_invalid_pot_account_form_input(self):
        self._login(self.user)
        pot_account_count_before: int = PotAccount.objects.count()
        bank_account_count_before: int = BankAccount.objects.count()
        form_input: dict[str, Any]= {
            "name": "Test Pot",
            "description": "This is a test pot",
            "currency": CurrencyType.GBP,
            "submit_type": MonetaryAccountType.POT
        }
        response: HttpResponse = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/monetary_accounts_form.html')
        pot_account_count_after: int = PotAccount.objects.count()
        bank_account_count_after: int = BankAccount.objects.count()
        self.assertEqual(pot_account_count_before, pot_account_count_after)
        self.assertEqual(bank_account_count_before, bank_account_count_after)
    
    def test_invalid_bank_account_form_input(self):
        self._login(self.user)
        pot_account_count_before: int = PotAccount.objects.count()
        bank_account_count_before: int = BankAccount.objects.count()
        form_input: dict[str, Any] = {
            "name": "Test Bank",
            "description": "This is a test bank",
            "currency": CurrencyType.GBP,
            "bank_name": "Best Test Bank",
            "account_number": "12345678",
            "sort_code": "123456",
            "iban": "GB1234567890112345",
            "interest_rate": 0,
            "submit_type": MonetaryAccountType.BANK
        }
        response: HttpResponse = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/monetary_accounts_form.html')
        pot_account_count_after: int = PotAccount.objects.count()
        bank_account_count_after: int = BankAccount.objects.count()
        self.assertEqual(pot_account_count_before, pot_account_count_after)
        self.assertEqual(bank_account_count_before, bank_account_count_after)


    def test_post_page_redirects_when_logged_out(self):
        form_input: dict[str, Any] = {'account_type': "Random"}
        response: HttpResponse = self.client.get(self.url, form_input, follow=True)
        self._assert_require_login(self.url)

    def test_get_page_redirects_when_logged_out(self):
        response: HttpResponse = self.client.get(self.url, follow=True)
        self._assert_require_login(self.url)