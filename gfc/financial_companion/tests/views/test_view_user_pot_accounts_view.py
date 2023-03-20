from django.urls import reverse
from .test_view_base import ViewTestCase
from financial_companion.models import User, PotAccount, BankAccount
from django.db.models import QuerySet


class ViewAccountsViewTestCase(ViewTestCase):
    """Tests of the user view pot accounts view."""

    def setUp(self):
        self.url: str = reverse('view_accounts')
        self.user: User = User.objects.get(username='@johndoe')
        self.account: PotAccount = PotAccount.objects.get(name='ghi')

    def test_view_accounts_url(self):
        self.assertEqual(self.url, '/view_accounts/')

    def test_get_view_accounts(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/view_accounts.html')
        pot_accounts: QuerySet[PotAccount] = response.context["pot_accounts"]
        for pot_account in pot_accounts:
            self.assertTrue(isinstance(pot_account, PotAccount))
        bank_accounts: list[BankAccount] = response.context["bank_accounts"]
        for bank_account in bank_accounts:
            self.assertTrue(isinstance(bank_account, BankAccount))

    def test_get_view_accounts_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)

    def test_view_accounts_contains_accounts_by_self(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertContains(response, self.account.id)

    def test_no_accounts_appear_in_more_than_one_list(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        pot_accounts: list[PotAccount] = response.context["pot_accounts"]
        bank_accounts: list[BankAccount] = response.context["bank_accounts"]
        self.assertFalse(bool(set(pot_accounts) & set(bank_accounts)))
