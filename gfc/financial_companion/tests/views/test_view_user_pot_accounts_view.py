from django.urls import reverse
from .test_view_base import ViewTestCase
from financial_companion.models import User, PotAccount

class ViewAccountsViewTestCase(ViewTestCase):
    """Tests of the user view pot accounts view."""

    def setUp(self):
        self.url = reverse('view_accounts')
        self.user = User.objects.get(username='@johndoe')
        self.account = PotAccount.objects.get(name='ghi')

    def test_view_accounts_url(self):
        self.assertEqual(self.url,'/view_accounts/')

    def test_get_view_accounts(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/view_accounts.html')

    def test_get_view_accounts_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)

    def test_view_accounts_contains_accounts_by_self(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertContains(response, self.account.id)
