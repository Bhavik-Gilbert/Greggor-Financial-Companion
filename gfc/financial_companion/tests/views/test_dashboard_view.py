from .test_view_base import ViewTestCase
from financial_companion.models import User, Account, PotAccount, Transaction, AbstractTransaction
from django.contrib.messages import get_messages
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
        for transaction in self.recent:
            self.assertContains(response, transaction.title.title())
            self.assertContains(
                response, transaction.category.name.capitalize())
            self.assertContains(response, transaction.amount)
            self.assertContains(
                response,
                transaction.sender_account.name.capitalize())
            self.assertContains(
                response,
                transaction.receiver_account.name.capitalize())
        self.assertTemplateUsed(
            response,
            'partials/dashboard/account_projection_graph.html'
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertLessEqual(len(messages), 3)
        self.assertTrue('Targets exceeded: ' in str(messages[0]))
