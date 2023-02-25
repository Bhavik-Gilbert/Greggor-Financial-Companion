from django.contrib.auth.hashers import check_password
from django.urls import reverse
from .test_view_base import ViewTestCase
from financial_companion.forms import TargetForm
from financial_companion.models import User, Account, AccountTarget


class EditAccountTargetViewTestCase(ViewTestCase):
    """Tests of the edit account target view."""

    def setUp(self):
        self.url = reverse('edit_account_target', kwargs={'pk': 1})
        self.test_user = User.objects.get(username='@johndoe')
        self.test_category = Account.objects.get(id=3)
        self.form_input = {
            'transaction_type': 'income',
            'timespan': 'month',
            'amount': 200.00,
            'currency': 'USD'
        }

    def test_edit_account_target_url(self):
        self.assertEqual(self.url, '/edit_target/account/1')

    def test_invalid_pk_entered(self):
        self._login(self.test_user)
        url: str = reverse(
            "edit_account_target", kwargs={
                "pk": 99999999})
        response: HttpResponse = self.client.get(url, follow=True)
        response_url: str = reverse("dashboard")
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, "pages/dashboard.html")

    def test_other_users_account_pk_entered(self):
        self._login(self.test_user)
        url: str = reverse(
            "edit_account_target", kwargs={
                "pk": 2})
        response: HttpResponse = self.client.get(url, follow=True)
        response_url: str = reverse("view_accounts")
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, "pages/view_accounts.html")

    def test_successful_edit_account_target_form_submission(self):
        self._login(self.test_user)
        before_count = AccountTarget.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = AccountTarget.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertTemplateUsed(response, 'pages/individual_account.html')

    def test_invalid_account_target_form_submission(self):
        self._login(self.test_user)
        self.form_input['transaction_type'] = ''
        before_count = AccountTarget.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = AccountTarget.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertTemplateUsed(response, 'pages/create_targets.html')

    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
