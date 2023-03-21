
from .test_view_base import ViewTestCase
from financial_companion.models import User
from financial_companion.helpers import get_data_for_account_projection
from django.urls import reverse


class ViewSavingsAccountsViewTestCase(ViewTestCase):
    """Tests of the Savings Accounts Projection view."""

    def setUp(self):
        self.url: str = reverse('view_savings_accounts')
        self.user: User = User.objects.get(username='@johndoe')

    def test_view_savings_accounts_url(self):
        self.assertEqual(self.url, '/view_savings_accounts/')

    def test_get_view_savings_accounts_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)

    def test_get_view_savings_accounts(self):
        self._login(self.user)
        self.response: HttpResponse = self.client.get(self.url)
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(
            self.response,
            'pages/view_savings_accounts.html')
        self.assertTemplateUsed(self.response,
                                'partials/dashboard/account_projection_graph.html'
                                )
        accountsProjections: dict[str,
                                  Any] = get_data_for_account_projection(self.user)
        self._assert_context_is_passed_in(accountsProjections)

    def _assert_context_is_passed_in(self, accountsProjections):
        for key in accountsProjections.keys():
            self.assertEqual(
                self.response.context[key], accountsProjections[key]
            )
