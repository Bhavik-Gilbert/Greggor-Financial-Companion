from .test_view_base import ViewTestCase
from financial_companion.forms import UserLogInForm
from financial_companion.models import User, PotAccount, Transaction
from django.urls import reverse


class FilterTransactionsViewTestCase(ViewTestCase):
    """Unit tests of the filter transactions request view"""

    def setUp(self):
        self.url = reverse(
            'filter_transaction_request', kwargs={
                "redirect_name": "view_transactions"})
        self.user = User.objects.get(username='@johndoe')

    def test_log_in_url(self):
        self.assertEqual(
            self.url,
            '/filter_transaction_request/view_transactions/')

    def test_post_when_all_button_is_clicked(self):
        self._login(self.user)
        self.form_data = {
            'all': True
        }
        response_url = reverse(
            'view_transactions', kwargs={
                'filter_type': "all"})
        response = self.client.post(self.url, self.form_data)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        response = self.client.post(response_url)
        self.assertTemplateUsed(response, 'pages/display_transactions.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, 'New Car')
        self.assertContains(response, 4)
        self.assertContains(response, 14999.99)
        self.assertContains(response, 'New Bike')
        self.assertContains(response, 5)
        self.assertContains(response, 499.99)

    def test_post_when_sent_button_is_clicked(self):
        self._login(self.user)
        self.form_data = {
            'sent': True
        }
        response_url = reverse(
            'view_transactions', kwargs={
                'filter_type': "sent"})
        response = self.client.post(self.url, self.form_data)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        response = self.client.post(response_url)
        self.assertTemplateUsed(response, 'pages/display_transactions.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, 'New Car')
        self.assertContains(response, 4)
        self.assertContains(response, 14999.99)

    def test_post_when_received_button_is_clicked(self):
        self._login(self.user)
        self.form_data = {
            'received': True
        }
        response_url = reverse(
            'view_transactions', kwargs={
                'filter_type': "received"})
        response = self.client.post(self.url, self.form_data)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        response = self.client.post(response_url)
        self.assertTemplateUsed(response, 'pages/display_transactions.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, 'New Bike')
        self.assertContains(response, 5)
        self.assertContains(response, 499.99)

    def test_post_when_random_input_is_given(self):
        self._login(self.user)
        self.form_data = {
            'other': True
        }
        response_url = reverse('dashboard')
        response = self.client.post(self.url, self.form_data)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        response = self.client.post(response_url)
        self.assertTemplateUsed(response, 'pages/dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
