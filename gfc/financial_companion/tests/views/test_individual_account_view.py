from .test_view_base import ViewTestCase
from financial_companion.models import User, Account, PotAccount, BankAccount
from django.http import HttpResponse
from django.urls import reverse
from django.db.models import Q


class IndividualAccountViewTestCase(ViewTestCase):
    """Unit tests of the individual category view"""

    def setUp(self):
        self.user: User = User.objects.get(username="@johndoe")
        self.account: PotAccount = PotAccount.objects.get_subclass(user=self.user, id=5)
        self.url: str = reverse("individual_account", kwargs={"pk": self.account.id, "filter_type": "all"})

    def test_valid_individual_account_url(self):
        self.assertEqual(self.url, f"/individual_account/{self.account.id}/all/")

    def test_valid_get_view_individual_account(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/individual_account.html")
        account: Account = response.context["account"]
        self.assertTrue(isinstance(account, PotAccount))

    
    def test_valid_account_belongs_to_user(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/individual_account.html")
    
    def test_invalid_account_does_not_belong_to_user(self):
        self._login(self.user)
        account: PotAccount = PotAccount.objects.get_subclass(~Q(user=self.user))
        url: str = reverse("individual_account", kwargs={"pk": account.id, "filter_type": "all"})
        response: HttpResponse = self.client.get(url, follow=True)
        response_url: str = reverse("dashboard")
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "pages/dashboard.html")

    def test_invalid_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)

    