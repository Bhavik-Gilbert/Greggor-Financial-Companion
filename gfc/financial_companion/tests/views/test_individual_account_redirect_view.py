from .test_view_base import ViewTestCase
from financial_companion.models import User, PotAccount
from django.http import HttpResponse
from django.urls import reverse


class IndividualAccountRedirectViewTestCase(ViewTestCase):
    """Unit tests of the individual account redirect view"""

    def setUp(self):
        self.user: User = User.objects.get(username="@johndoe")
        self.account: PotAccount = PotAccount.objects.get_subclass(user=self.user, id=3)
        self.url: str = reverse("individual_account", kwargs={"pk": self.account.id})

    def test_valid_individual_account_redirect_url(self):
        self.assertEqual(self.url, f"/individual_account/{self.account.id}/")

    def test_valid_get_individual_account_redirect(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url: str = reverse("individual_account", kwargs={"pk": self.account.id, "filter_type": "all"})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "pages/individual_account.html")

    def test_invalid_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)