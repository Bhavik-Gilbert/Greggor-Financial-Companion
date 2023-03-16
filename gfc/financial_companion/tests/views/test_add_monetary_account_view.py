from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from typing import Any

from .test_view_base import ViewTestCase
from financial_companion.forms import PotAccountForm, BankAccountForm, RegularAccountForm
from financial_companion.models import User, PotAccount, BankAccount, Account
from financial_companion.helpers import AccountType, CurrencyType
from decimal import Decimal


class AddMonetaryAccountViewTestCase(ViewTestCase):
    """Unit tests of the add monetary account view"""

    def setUp(self) -> None:
        self.user: User = User.objects.get(username="@johndoe")
        self.url: str = reverse(f"add_monetary_account")

    def test_valid_page_url(self) -> None:
        self.assertEqual(self.url, "/add_monetary_account/")

    def test_valid_get_page(self) -> None:
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/monetary_accounts_form.html")
        form: PotAccountForm = response.context["form"]
        self.assertTrue(isinstance(form, RegularAccountForm))
        form_toggle: bool = response.context["form_toggle"]
        self.assertTrue(form_toggle)
        account_type: AccountType = response.context["account_type"]
        self.assertEqual(account_type, AccountType.REGULAR)
        monetary_account_types: AccountType = response.context["monetary_account_types"]
        self.assertEqual(monetary_account_types, AccountType)
        self.assertFalse(form.is_bound)

    def test_valid_post_account_type_regular(self) -> None:
        self._login(self.user)
        form_input: dict[str, Any] = {"account_type": AccountType.REGULAR}
        response: HttpResponse = self.client.post(self.url, form_input)
        account_type: AccountType = response.context["account_type"]
        self.assertEqual(account_type, AccountType.REGULAR)
        form: RegularAccountForm = response.context["form"]
        self.assertTrue(isinstance(form, RegularAccountForm))

    def test_valid_post_account_type_pot(self) -> None:
        self._login(self.user)
        form_input: dict[str, Any] = {"account_type": AccountType.POT}
        response: HttpResponse = self.client.post(self.url, form_input)
        account_type: AccountType = response.context["account_type"]
        self.assertEqual(account_type, AccountType.POT)
        form: PotAccountForm = response.context["form"]
        self.assertTrue(isinstance(form, PotAccountForm))

    def test_valid_post_account_type_bank(self) -> None:
        self._login(self.user)
        form_input: dict[str, Any] = {"account_type": AccountType.BANK}
        response: HttpResponse = self.client.post(self.url, form_input)
        account_type: AccountType = response.context["account_type"]
        self.assertEqual(account_type, AccountType.BANK)
        form: PotAccountForm = response.context["form"]
        self.assertTrue(isinstance(form, BankAccountForm))

    def test_valid_regular_account_form_input(self) -> None:
        self._login(self.user)
        regular_account_count_before: int = Account.objects.count()
        pot_account_count_before: int = PotAccount.objects.count()
        bank_account_count_before: int = BankAccount.objects.count()
        form_input: dict[str, Any] = {
            "name": "Test Regular",
            "description": "This is a test pot",
            "submit_type": AccountType.REGULAR
        }
        response: HttpResponse = self.client.post(
            self.url, form_input, follow=True)
        response_url: str = reverse("view_accounts")
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, "pages/view_accounts.html")
        regular_account_count_after: int = Account.objects.count()
        pot_account_count_after: int = PotAccount.objects.count()
        bank_account_count_after: int = BankAccount.objects.count()
        self.assertEqual(
            regular_account_count_before + 1,
            regular_account_count_after)
        self.assertEqual(pot_account_count_before, pot_account_count_after)
        self.assertEqual(bank_account_count_before, bank_account_count_after)

    def test_valid_pot_account_form_input(self) -> None:
        self._login(self.user)
        pot_account_count_before: int = PotAccount.objects.count()
        bank_account_count_before: int = BankAccount.objects.count()
        form_input: dict[str, Any] = {
            "name": "Test Pot",
            "description": "This is a test pot",
            "balance": Decimal("99.99"),
            "currency": CurrencyType.GBP,
            "submit_type": AccountType.POT
        }
        response: HttpResponse = self.client.post(
            self.url, form_input, follow=True)
        response_url: str = reverse("view_accounts")
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, "pages/view_accounts.html")
        pot_account_count_after: int = PotAccount.objects.count()
        bank_account_count_after: int = BankAccount.objects.count()
        self.assertEqual(pot_account_count_before + 1, pot_account_count_after)
        self.assertEqual(bank_account_count_before, bank_account_count_after)

    def test_valid_bank_account_form_input(self) -> None:
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
            "submit_type": AccountType.BANK
        }
        response: HttpResponse = self.client.post(
            self.url, form_input, follow=True)
        response_url: str = reverse("view_accounts")
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, "pages/view_accounts.html")
        pot_account_count_after: int = PotAccount.objects.count()
        bank_account_count_after: int = BankAccount.objects.count()
        self.assertEqual(pot_account_count_before + 1, pot_account_count_after)
        self.assertEqual(
            bank_account_count_before + 1,
            bank_account_count_after)

    def test_invalid_regular_account_form_input(self) -> None:
        self._login(self.user)
        regualr_account_count_before: int = Account.objects.count()
        pot_account_count_before: int = PotAccount.objects.count()
        bank_account_count_before: int = BankAccount.objects.count()
        form_input: dict[str, Any] = {
            "name": "Test regular",
            "description": "This is a test account",
            "currency": CurrencyType.GBP,
            "submit_type": AccountType.POT
        }
        response: HttpResponse = self.client.post(
            self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/monetary_accounts_form.html")
        regualr_account_count_after: int = Account.objects.count()
        pot_account_count_after: int = PotAccount.objects.count()
        bank_account_count_after: int = BankAccount.objects.count()
        self.assertEqual(
            regualr_account_count_before,
            regualr_account_count_after)
        self.assertEqual(pot_account_count_before, pot_account_count_after)
        self.assertEqual(bank_account_count_before, bank_account_count_after)

    def test_invalid_pot_account_form_input(self) -> None:
        self._login(self.user)
        pot_account_count_before: int = PotAccount.objects.count()
        bank_account_count_before: int = BankAccount.objects.count()
        form_input: dict[str, Any] = {
            "name": "Test Pot",
            "description": "This is a test pot",
            "currency": CurrencyType.GBP,
            "submit_type": AccountType.POT
        }
        response: HttpResponse = self.client.post(
            self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/monetary_accounts_form.html")
        pot_account_count_after: int = PotAccount.objects.count()
        bank_account_count_after: int = BankAccount.objects.count()
        self.assertEqual(pot_account_count_before, pot_account_count_after)
        self.assertEqual(bank_account_count_before, bank_account_count_after)

    def test_invalid_bank_account_form_input(self) -> None:
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
            "submit_type": AccountType.BANK
        }
        response: HttpResponse = self.client.post(
            self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/monetary_accounts_form.html")
        pot_account_count_after: int = PotAccount.objects.count()
        bank_account_count_after: int = BankAccount.objects.count()
        self.assertEqual(pot_account_count_before, pot_account_count_after)
        self.assertEqual(bank_account_count_before, bank_account_count_after)

    def test_vaild_post_page_redirects_when_logged_out(self) -> None:
        form_input: dict[str, Any] = {"account_type": "Random"}
        response: HttpResponse = self.client.get(
            self.url, form_input, follow=True)
        self._assert_require_login(self.url)

    def test_valid_get_page_redirects_when_logged_out(self) -> None:
        response: HttpResponse = self.client.get(self.url, follow=True)
        self._assert_require_login(self.url)
