from .test_view_base import ViewTestCase
from financial_companion.models import User
from django.urls import reverse


class DispalyTransactionRedirectViewTestCase(ViewTestCase):
    """Unit tests of the display transactions redirect view"""

    def setUp(self):
        self.url = reverse('view_transactions_redirect')
        self.user = User.objects.get(username='@johndoe')

    def test_valid_log_in_url(self):
        self.assertEqual(self.url,'/view_transactions/')
    
    def test_valid_get_view_transactions_redirect(self):
        self._login(self.user)
        response = self.client.get(self.url, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('view_transactions',kwargs={'filter_type': "all"})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'pages/display_transactions.html')
        
    def test_invalid_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)