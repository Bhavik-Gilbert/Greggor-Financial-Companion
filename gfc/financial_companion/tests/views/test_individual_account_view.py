from .test_view_base import ViewTestCase
from financial_companion.models import User, Account, PotAccount, AccountTarget
from django.http import HttpResponse
from django.urls import reverse
from django.db.models import Q
from financial_companion.templatetags import get_completeness


class IndividualAccountViewTestCase(ViewTestCase):
    """Unit tests of the individual account view"""

    def setUp(self):
        self.user: User = User.objects.get(username="@johndoe")
        self.account: PotAccount = PotAccount.objects.get_subclass(
            user=self.user, id=3)
        self.url: str = reverse(
            "individual_account",
            kwargs={
                "pk": self.account.id,
                "filter_type": "all"})
        self.redirect_url: str = reverse(
            "individual_account_redirect", kwargs={
                "pk": self.account.id})

    def test_valid_individual_account_url(self):
        self.assertEqual(
            self.url,
            f"/individual_account/{self.account.id}/all/")

    def test_valid_individual_account_redirect_url(self):
        self.assertEqual(
            self.redirect_url,
            f"/individual_account/{self.account.id}/")

    def test_valid_get_individual_account_redirect(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.redirect_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/individual_account.html")
        account: Account = response.context["account"]
        self.assertTrue(isinstance(account, PotAccount))

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
        accounts: PotAccount = PotAccount.objects.filter(
            ~Q(user=self.user))
        url: str = reverse(
            "individual_account",
            kwargs={
                "pk": accounts[0].id,
                "filter_type": "all"})
        response: HttpResponse = self.client.get(url, follow=True)
        response_url: str = reverse("dashboard")
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, "pages/dashboard.html")

    def test_valid_account_has_targets(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/individual_account.html")
        account_targets: Account = response.context["account_targets"]
        for target in account_targets:
            self.assertTrue(isinstance(target, AccountTarget))
            self.assertContains(response, target.target_type.capitalize())
            self.assertContains(response, target.timespan.capitalize())
            self.assertContains(response, get_completeness(target))
            self.assertContains(response, target.currency.upper())
            self.assertContains(response, target.amount)
        self.assertGreater(len(account_targets), 0)

    def test_valid_account_does_not_have_targets(self):
        self._login(self.user)
        account: PotAccount = PotAccount.objects.get_subclass(
            user=self.user, id=5)
        url: str = reverse(
            "individual_account",
            kwargs={
                "pk": account.id,
                "filter_type": "all"})
        response: HttpResponse = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/individual_account.html")
        account_targets: Account = response.context["account_targets"]
        self.assertEqual(len(account_targets), 0)

    def test_invalid_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)

    def test_invalid_filter_type_redirect_reset_to_all(self):
        self._login(self.user)
        url: str = reverse(
            "individual_account",
            kwargs={
                "pk": self.account.id,
                "filter_type": "invalid"})
        response: HttpResponse = self.client.get(url, follow=True)
        response_url: str = reverse("dashboard")
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
