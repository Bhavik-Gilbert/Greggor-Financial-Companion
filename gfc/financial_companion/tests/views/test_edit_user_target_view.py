from django.contrib.auth.hashers import check_password
from django.urls import reverse
from .test_view_base import ViewTestCase
from financial_companion.forms import TargetForm
from financial_companion.models import User, UserTarget
from typing import Any
from django.http import HttpRequest, HttpResponse

class EditUserTargetViewTestCase(ViewTestCase):
    """Tests of the edit user target view."""

    def setUp(self) -> None:
        self.url: str = reverse('edit_user_target', kwargs={'pk': 1})
        self.test_user: User = User.objects.get(username='@johndoe')
        self.form_input: dict[str, Any] = {
            'target_type': 'income',
            'timespan': 'month',
            'amount': 200.00,
            'currency': 'USD'
        }

    def test_edit_user_target_url(self) -> None:
        self.assertEqual(self.url, '/edit_target/user/1')

    def test_invalid_pk_entered(self) -> None:
        self._login(self.test_user)
        url: str = reverse(
            "edit_user_target", kwargs={
                "pk": 99999999})
        response: HttpResponse = self.client.get(url, follow=True)
        response_url: str = reverse("dashboard")
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, "pages/dashboard.html")

    def test_other_users_user_target_pk_entered(self) -> None:
        self._login(self.test_user)
        url: str = reverse(
            "edit_user_target", kwargs={
                "pk": 2})
        response: HttpResponse = self.client.get(url, follow=True)
        response_url: str = reverse("dashboard")
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, "pages/dashboard.html")

    def test_successful_edit_user_target_form_submission(self) -> None:
        self._login(self.test_user)
        before_count: int = UserTarget.objects.count()
        response: HttpResponse = self.client.post(self.url, self.form_input, follow=True)
        after_count: int = UserTarget.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertTemplateUsed(response, 'pages/view_targets.html')

    def test_invalid_user_target_form_submission(self) -> None:
        self._login(self.test_user)
        self.form_input['target_type']: str = ''
        before_count: int = UserTarget.objects.count()
        response: HttpResponse = self.client.post(self.url, self.form_input, follow=True)
        after_count: int = UserTarget.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertTemplateUsed(response, 'pages/create_targets.html')

    def test_get_view_redirects_when_not_logged_in(self) -> None:
        self._assert_require_login(self.url)
