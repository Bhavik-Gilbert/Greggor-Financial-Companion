from django.http import HttpResponse
from django.urls import reverse
from typing import Any

from .test_view_base import ViewTestCase
from financial_companion.forms import PotAccountForm, BankAccountForm
from financial_companion.models import User, PotAccount, BankAccount
from financial_companion.helpers import MonetaryAccountType, CurrencyType
from decimal import Decimal

class AddMonetaryAccountViewTestCase(ViewTestCase):
    """Unit tests of the edit monetary account view"""

    def setUp(self):
        self.pot_account: PotAccount = PotAccount.objects.get(id=4)
        self.bank_account: BankAccount = BankAccount.objects.get(id=5)
        self.pot_user: User = User.objects.get(id=self.pot_account.user.id)
        self.bank_user: User = User.objects.get(id=self.bank_account.user.id)
        self.pot_url: str = reverse("edit_monetary_account", kwargs={"pk": self.pot_account.id})
        self.bank_url: str = reverse("edit_monetary_account", kwargs={"pk": self.bank_account.id})

    def test_valid_pot_page_url(self):
        self.assertEqual(self.pot_url, f"/edit_monetary_account/{self.pot_account.id}/")
    
    def test_valid_bank_page_url(self):
        self.assertEqual(self.bank_url, f"/edit_monetary_account/{self.bank_account.id}/")

    def test_valid_get_pot_page(self):
        self._login(self.pot_user)
        response: HttpResponse = self.client.get(self.pot_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/monetary_accounts_form.html")
        form: PotAccountForm = response.context["form"]
        self.assertTrue(isinstance(form, PotAccountForm))
        form_toggle: bool = response.context["form_toggle"]
        self.assertFalse(form_toggle)
        account_type: MonetaryAccountType = response.context["account_type"]
        self.assertEqual(account_type, MonetaryAccountType.POT)
        monetary_account_types: MonetaryAccountType = response.context["monetary_account_types"]
        self.assertEqual(monetary_account_types, MonetaryAccountType)
        self.assertFalse(form.is_bound)
    
    def test_valid_get_bank_page(self):
        self._login(self.bank_user)
        response: HttpResponse = self.client.get(self.bank_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/monetary_accounts_form.html")
        form: BankAccountForm = response.context["form"]
        self.assertTrue(isinstance(form, BankAccountForm))
        form_toggle: bool = response.context["form_toggle"]
        self.assertFalse(form_toggle)
        account_type: MonetaryAccountType = response.context["account_type"]
        self.assertEqual(account_type, MonetaryAccountType.BANK)
        monetary_account_types: MonetaryAccountType = response.context["monetary_account_types"]
        self.assertEqual(monetary_account_types, MonetaryAccountType)
        self.assertFalse(form.is_bound)
    
    def test_valid_pot_account_form_input(self):
        self._login(self.pot_user)
        pot_account_count_before: int = PotAccount.objects.count()
        bank_account_count_before: int = BankAccount.objects.count()
        form_input: dict[str, Any]= {
            "name": "Test Pot",
            "description": "This is a test pot",
            "balance": Decimal("99.99"),
            "currency": CurrencyType.GBP,
            "submit_type": MonetaryAccountType.POT
        }
        response: HttpResponse = self.client.post(self.pot_url, form_input, follow=True)
        response_url: str = reverse("dashboard")
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "pages/dashboard.html")
        pot_account_count_after: int = PotAccount.objects.count()
        bank_account_count_after: int = BankAccount.objects.count()
        self.assertEqual(pot_account_count_before, pot_account_count_after)
        self.assertEqual(bank_account_count_before, bank_account_count_after)
    
    def test_valid_bank_account_form_input(self):
        self._login(self.bank_user)
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
        response: HttpResponse = self.client.post(self.bank_url, form_input, follow=True)
        response_url: str = reverse("dashboard")
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "pages/dashboard.html")
        pot_account_count_after: int = PotAccount.objects.count()
        bank_account_count_after: int = BankAccount.objects.count()
        self.assertEqual(pot_account_count_before, pot_account_count_after)
        self.assertEqual(bank_account_count_before, bank_account_count_after)
    
    def test_invalid_pot_account_form_input(self):
        self._login(self.pot_user)
        pot_account_count_before: int = PotAccount.objects.count()
        bank_account_count_before: int = BankAccount.objects.count()
        form_input: dict[str, Any]= {
            "name": "Test Pot",
            "description": "This is a test pot",
            "currency": CurrencyType.GBP,
            "submit_type": MonetaryAccountType.POT
        }
        response: HttpResponse = self.client.post(self.pot_url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/monetary_accounts_form.html")
        pot_account_count_after: int = PotAccount.objects.count()
        bank_account_count_after: int = BankAccount.objects.count()
        self.assertEqual(pot_account_count_before, pot_account_count_after)
        self.assertEqual(bank_account_count_before, bank_account_count_after)
    
    def test_invalid_bank_account_form_input(self):
        self._login(self.bank_user)
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
        response: HttpResponse = self.client.post(self.bank_url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/monetary_accounts_form.html")
        pot_account_count_after: int = PotAccount.objects.count()
        bank_account_count_after: int = BankAccount.objects.count()
        self.assertEqual(pot_account_count_before, pot_account_count_after)
        self.assertEqual(bank_account_count_before, bank_account_count_after)


    def test_valid_post_pot_page_redirects_when_logged_out(self):
        form_input: dict[str, Any] = {"account_type": "Random"}
        response: HttpResponse = self.client.get(self.pot_url, form_input, follow=True)
        self._assert_require_login(self.pot_url)
    
    def test_valid_post_bank_page_redirects_when_logged_out(self):
        form_input: dict[str, Any] = {"account_type": "Random"}
        response: HttpResponse = self.client.get(self.bank_url, form_input, follow=True)
        self._assert_require_login(self.bank_url)

    def test_valid_get_pot_page_redirects_when_logged_out(self):
        response: HttpResponse = self.client.get(self.pot_url, follow=True)
        self._assert_require_login(self.pot_url)

    def test_valid_get_bank_page_redirects_when_logged_out(self):
        response: HttpResponse = self.client.get(self.bank_url, follow=True)
        self._assert_require_login(self.bank_url)
    
    def test_invalid_post_pot_page_logged_in_user_must_be_account_holder(self):
        self._login(self.bank_user)
        self.assertNotEqual(self.pot_account.user.id, self.bank_user.id)
        form_input: dict[str, Any]= {
            "name": "Test Pot",
            "description": "This is a test pot",
            "currency": CurrencyType.GBP,
            "submit_type": MonetaryAccountType.POT
        }
        response: HttpResponse = self.client.post(self.pot_url, form_input, follow=True)
        response_url: str = reverse("dashboard")
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "pages/dashboard.html")
    
    def test_invalid_get_pot_page_logged_in_user_must_be_account_holder(self):
        self._login(self.bank_user)
        self.assertNotEqual(self.pot_account.user.id, self.bank_user.id)
        response: HttpResponse = self.client.post(self.pot_url, follow=True)
        response_url: str = reverse("dashboard")
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "pages/dashboard.html")

    
    def test_invalid_post_bank_page_logged_in_user_must_be_account_holder(self):
        self._login(self.pot_user)
        self.assertNotEqual(self.bank_account.user.id, self.pot_user.id)
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
        response: HttpResponse = self.client.post(self.bank_url, form_input, follow=True)
        response_url: str = reverse("dashboard")
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "pages/dashboard.html")
    
    def test_invalid_get_bank_page_loggeed_in_user_must_be_account_holder(self):
        self._login(self.pot_user)
        self.assertNotEqual(self.bank_account.user.id, self.pot_user.id)
        response: HttpResponse = self.client.post(self.bank_url, follow=True)
        response_url: str = reverse("dashboard")
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "pages/dashboard.html")