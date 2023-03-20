from django.urls import reverse
from .test_view_base import ViewTestCase
from financial_companion.forms import TargetForm
from financial_companion.models import User, UserTarget
from typing import Any
from django.http import HttpResponse


class CreateUserTargetViewTestCase(ViewTestCase):
    """Tests of the create user target view."""

    def setUp(self) -> None:
        self.url: str = reverse('create_user_target')
        self.test_user: User = User.objects.get(username='@johndoe')
        self.form_input: dict[str, Any] = {
            'target_type': 'income',
            'timespan': 'month',
            'amount': 200.00,
            'currency': 'USD'
        }

    def test_create_user_target_url(self) -> None:
        self.assertEqual(self.url, '/create_target/user/')

    def test_successful_user_target_form_submission(self) -> None:
        self._login(self.test_user)
        before_count: int = UserTarget.objects.count()
        response: HttpResponse = self.client.post(
            self.url, self.form_input, follow=True)
        after_count: int = UserTarget.objects.count()
        self.assertEqual(after_count, before_count + 1)
        self.assertTemplateUsed(response, 'pages/view_targets.html')

    def test_invalid_account_target_form_submission(self) -> None:
        self._login(self.test_user)
        self.form_input['target_type']: str = ''
        before_count: int = UserTarget.objects.count()
        response: HttpResponse = self.client.post(
            self.url, self.form_input, follow=True)
        after_count: int = UserTarget.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertTemplateUsed(response, 'pages/create_targets.html')

    def test_get_view_redirects_when_not_logged_in(self) -> None:
        self._assert_require_login(self.url)
