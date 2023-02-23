from django.contrib.auth.hashers import check_password
from django.urls import reverse
from .test_view_base import ViewTestCase
from financial_companion.forms import TargetForm
from financial_companion.models import User, UserTarget


class CreateUserTargetViewTestCase(ViewTestCase):
    """Tests of the create target user view."""

    def setUp(self):
        self.url = reverse('create_user_target')
        self.test_user = User.objects.get(username='@johndoe')
        self.form_input = {
            'transaction_type': 'income',
            'timespan': 'month',
            'amount': 200.00,
            'currency': 'USD'
        }

    def test_create_user_target_url(self):
        self.assertEqual(self.url, '/create_target/user/')

    def test_successful_user_target_form_submission(self):
        self._login(self.test_user)
        before_count = UserTarget.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = UserTarget.objects.count()
        self.assertEqual(after_count, before_count + 1)
        self.assertTemplateUsed(response, 'pages/dashboard.html')

    def test_invalid_account_target_form_submission(self):
        self._login(self.test_user)
        self.form_input['transaction_type'] = ''
        before_count = UserTarget.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = UserTarget.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertTemplateUsed(response, 'pages/create_targets.html')

    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
