from .test_view_base import ViewTestCase
from financial_companion.models import User, Account, PotAccount, Transaction, AbstractTransaction
from django.urls import reverse


class DashboardViewTestCase(ViewTestCase):
    """Tests of the user dashboard view."""

    def setUp(self):
        self.url = reverse('dashboard')
        self.user = User.objects.get(username='@johndoe')
        self.account = PotAccount.objects.get(name='ghi')
        user_transactions = []
        user_transactions = [
            *
            user_transactions,
            *
            Transaction.objects.filter(
                sender_account=self.account),
            *
            Transaction.objects.filter(
                receiver_account=self.account)]
        self.recent = user_transactions[0:3]

    def test_dashboard_url(self):
        self.assertEqual(self.url, '/dashboard/')

    def test_get_dashboard_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)

    def test_get_dashboard(self):
        self._login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/dashboard.html')

    def test_dashboard_displays_desired_info(self):
        self._login(self.user)
        response = self.client.get(self.url)
        self.assertContains(response, self.user.full_name().title())
        self.assertContains(response, self.account.name.capitalize())
        self.assertContains(response, self.account.description.capitalize())
        self.assertContains(response, self.account.balance)
        self.assertContains(response, self.recent[0].title.capitalize())
        self.assertContains(
            response, self.recent[0].category.name.capitalize())
        self.assertContains(response, self.recent[0].amount)
        self.assertContains(
            response,
            self.recent[0].sender_account.name.capitalize())
        self.assertContains(
            response,
            self.recent[0].receiver_account.name.capitalize())
        self.assertTemplateUsed(
            response,
            'partials/dashboard/account_projection_graph.html'
        )