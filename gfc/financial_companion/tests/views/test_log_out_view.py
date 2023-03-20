from django.urls import reverse
from .test_view_base import ViewTestCase
from financial_companion.models import User


class LogOutViewTestCase(ViewTestCase):
    """Tests of the log out view."""

    def setUp(self):
        self.url = reverse('log_out')
        self.user = User.objects.get(username='@johndoe')

    def test_log_out_url(self):
        self.assertEqual(self.url, '/log_out/')

    def test_get_log_out(self):
        self._login(self.user)
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        response_url = reverse('home')
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, 'pages/index.html')
        self.assertFalse(self._is_logged_in())

    def test_get_logout_redirects_when_logged_out(self):
        self._assert_require_login(self.url)
