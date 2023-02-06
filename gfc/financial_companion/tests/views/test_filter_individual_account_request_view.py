from .test_view_base import ViewTestCase
from financial_companion.forms import UserLogInForm
from financial_companion.models import User, PotAccount, Transaction
from django.urls import reverse


class FilterIndividualAccountViewTestCase(ViewTestCase):
    """Unit tests of the filter transactions request view"""

    def setUp(self):
        self.user: User = User.objects.get(username="@johndoe")
        self.account: PotAccount = PotAccount.objects.get_subclass(user=self.user, id=5)
        self.url: str = reverse("filter_individual_account_request", kwargs={"pk": self.account.id})
        

    def test_log_in_url(self):
        self.assertEqual(self.url,'/filter_individual_account_request/5')
    
    def test_post_when_all_button_is_clicked(self):
        self._login(self.user)
        self.form_data = {
            'all': True
        }
        response_url = reverse('individual_account',kwargs={"pk": self.account.id, 'filter_type': "all"})
        response = self.client.post(self.url, self.form_data)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        response = self.client.post(response_url)
        self.assertTemplateUsed(response, 'pages/individual_account.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, 'New glasses')
        self.assertContains(response, 6)
        self.assertContains(response, 299.99)
        self.assertContains(response, 'old laptop bag')
        self.assertContains(response, 7)
        self.assertContains(response, 89.99)
        self.assertContains(response, 'old phone')
        self.assertContains(response, 8)
        self.assertContains(response, 499.99)
    
    def test_post_when_sent_button_is_clicked(self):
        self._login(self.user)
        self.form_data = {
            'sent': True
        }
        response_url = reverse('individual_account',kwargs={"pk": self.account.id, 'filter_type': "sent"})
        response = self.client.post(self.url, self.form_data)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        response = self.client.post(response_url)
        self.assertTemplateUsed(response, 'pages/individual_account.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, 'New glasses')
        self.assertContains(response, 8)
        self.assertContains(response, 299.99)
    
    def test_post_when_received_button_is_clicked(self):
        self._login(self.user)
        self.form_data = {
            'received': True
        }
        response_url = reverse('individual_account',kwargs={"pk": self.account.id, 'filter_type': "received"})
        response = self.client.post(self.url, self.form_data)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        response = self.client.post(response_url)
        self.assertTemplateUsed(response, 'pages/individual_account.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, 'old laptop bag')
        self.assertContains(response, 7)
        self.assertContains(response, 89.99)
        self.assertContains(response, 'old phone')
        self.assertContains(response, 8)
        self.assertContains(response, 499.99)
    
    def test_post_when_random_input_is_given(self):
        self._login(self.user)
        self.form_data = {
            'other': True
        }
        response_url = reverse('dashboard')
        response = self.client.post(self.url, self.form_data)
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        response = self.client.post(response_url)
        self.assertTemplateUsed(response, 'pages/dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
    
    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)

    