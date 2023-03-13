from .test_view_base import ViewTestCase
from financial_companion.forms import UserLogInForm
from financial_companion.models import User, Transaction
from django.urls import reverse


class DisplayTransactionsViewTestCase(ViewTestCase):
    """Unit tests of the display transactions view"""

    def setUp(self):
        self.url = reverse('view_transactions', kwargs={'filter_type': "all"})
        self.url_redirect = reverse('view_transactions_redirect')
        self.user = User.objects.get(username='@johndoe')

    def test_display_transactions_url(self):
        self.assertEqual(self.url, '/view_transactions/all')

    def test_get_when_all_filter_is_applied(self):
        self._login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/display_transactions.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, 'New Car')
        self.assertContains(response, 4)
        self.assertContains(response, 14999.99)
        self.assertContains(response, 'New Bike')
        self.assertContains(response, 5)
        self.assertContains(response, 499.99)
        
    def test_valid_display_transactions_redirect_url(self):
        self.assertEqual(self.url_redirect, '/view_transactions/')

    def test_valid_get_view_transactions_redirect(self):
        self._login(self.user)
        response = self.client.get(self.url_redirect)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/display_transactions.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, 'New Car')
        self.assertContains(response, 4)
        self.assertContains(response, 14999.99)
        self.assertContains(response, 'New Bike')
        self.assertContains(response, 5)
        self.assertContains(response, 499.99)

    def test_get_when_sent_filter_is_applied(self):
        self._login(self.user)
        self.url = reverse('view_transactions', kwargs={'filter_type': "sent"})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/display_transactions.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, 'New Car')
        self.assertContains(response, 4)
        self.assertContains(response, 14999.99)

    def test_get_when_received_filter_is_applied(self):
        self._login(self.user)
        self.url = reverse(
            'view_transactions', kwargs={
                'filter_type': "received"})
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/display_transactions.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, 'New Bike')
        self.assertContains(response, 5)
        self.assertContains(response, 499.99)

    def test_get_when_incorrect_filter_is_applied(self):
        self._login(self.user)
        self.url = reverse(
            'view_transactions', kwargs={
                'filter_type': "incorrect"})
        response_url = reverse('dashboard')
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)

    def test_if_invalid_page_number_given(self):
        self._login(self.user)
        self.url = f'{self.url}?page=-21.20'
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, 'New Car')
        self.assertContains(response, 4)
        self.assertContains(response, 14999.99)
        self.assertContains(response, 'New Bike')
        self.assertContains(response, 5)
        self.assertContains(response, 499.99)

    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
