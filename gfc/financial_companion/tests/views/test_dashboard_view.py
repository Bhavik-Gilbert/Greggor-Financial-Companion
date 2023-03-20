from .test_view_base import ViewTestCase
from financial_companion.models import User, PotAccount, Transaction
from django.contrib.messages import get_messages
from django.urls import reverse
from django.db.models import QuerySet
from django.http import HttpResponse
from django.contrib.messages.storage.base import Message


class DashboardViewTestCase(ViewTestCase):
    """Tests of the user dashboard view."""

    def setUp(self) -> None:
        self.url: str = reverse('dashboard')
        self.user: User = User.objects.get(username='@johndoe')
        self.account: PotAccount = PotAccount.objects.get(name='ghi')
        user_transactions: list = []
        user_transactions: QuerySet[Transaction] = [
            *
            user_transactions,
            *
            Transaction.objects.filter(
                sender_account=self.account),
            *
            Transaction.objects.filter(
                receiver_account=self.account)]
        self.recent: list[Transaction] = user_transactions[0:3]

    def test_dashboard_url(self) -> None:
        self.assertEqual(self.url, '/dashboard/')

    def test_get_dashboard_redirects_when_not_logged_in(self) -> None:
        self._assert_require_login(self.url)

    def test_get_dashboard(self) -> None:
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/dashboard.html')

    def test_dashboard_displays_desired_info(self) -> None:
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertContains(response, self.user.full_name().title())
        self.assertContains(response, self.account.name.title())
        self.assertContains(response, self.account.description.title())
        self.assertContains(response, self.account.balance)
        for transaction in self.recent:
            self.assertContains(response, transaction.title.title())
            self.assertContains(
                response, transaction.category.name.title())
            self.assertContains(response, transaction.amount)
            self.assertContains(
                response,
                transaction.sender_account.name.title())
            self.assertContains(
                response,
                transaction.receiver_account.name.title())
        self.assertTemplateUsed(
            response,
            'partials/dashboard/account_projection_graph_card.html'
        )
        messages: list[Message] = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 2)
        self.assertLessEqual(len(messages), 3)
        self.assertTrue('Targets completed: ' in str(messages[0]))
        self.assertTrue('Targets nearly exceeded: ' in str(messages[1]))
