from django.contrib.auth.hashers import check_password
from django.urls import reverse

from .test_view_base import ViewTestCase
from financial_companion.forms import UserLogInForm
from financial_companion.models import User


class LogInViewTestCase(ViewTestCase):
    """Unit tests of the log in view"""

    def setUp(self):
        self.url = reverse('log_in')
        self.user = User.objects.get(username='@johndoe')

    def test_log_in_url(self):
        self.assertEqual(self.url, '/log_in/')

    def test_get_log_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserLogInForm))
        self.assertFalse(form.is_bound)

    def test_successful_log_in(self):
        form_input = {'username': '@johndoe', 'password': 'Password123'}
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('dashboard')
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, 'pages/dashboard.html')

    def test_unsuccessful_log_in(self):
        form_input = {'username': '@johndoe', 'password': 'WrongPassword123'}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserLogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_invalid_form_for_log_in(self):
        wrong_form_input = {
            'username': 'johndoe',
            'password': 'WrongPassword123'}
        response = self.client.post(self.url, wrong_form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserLogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_get_login_redirects_when_logged_in(self):
        self._login(self.user)
        self._assert_require_logout(self.url)
