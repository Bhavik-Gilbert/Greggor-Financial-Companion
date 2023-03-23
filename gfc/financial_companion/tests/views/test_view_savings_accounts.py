from django.http import HttpResponse
from .test_view_base import ViewTestCase
from financial_companion.models import User
from financial_companion.helpers import get_data_for_account_projection
from django.urls import reverse
from typing import Any


class ViewSavingsAccountsViewTestCase(ViewTestCase):
    """Tests of the savings accounts projection view."""

    def setUp(self):
        super().setUp()
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
        account_projections: dict[str,
                                  Any] = get_data_for_account_projection(self.user)
        self._assert_context_is_passed_in(account_projections)

    def _assert_context_is_passed_in(self, account_projections):
        for key in account_projections.keys():
            self.assertEqual(
                self.response.context[key], account_projections[key]
            )
