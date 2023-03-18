from django.contrib.auth.hashers import check_password
from django.urls import reverse
from .test_view_base import ViewTestCase
from financial_companion.forms import TargetForm
from financial_companion.models import User, Category, CategoryTarget
from django.http import HttpRequest, HttpResponse
from typing import Any
from django.contrib.messages.storage.base import Message

class CreateCategoryTargetViewTestCase(ViewTestCase):
    """Tests of the create category target view."""

    def setUp(self) -> None:
        self.url: str = reverse('create_category_target', kwargs={'pk': 1})
        self.test_user: User = User.objects.get(username='@johndoe')
        self.test_category: Category = Category.objects.get(id=1)
        self.test_category_target: CategoryTarget = CategoryTarget.objects.get(id=1)
        self.form_input: dict[str, Any] = {
            'target_type': 'income',
            'timespan': 'month',
            'amount': 200.00,
            'currency': 'USD'
        }

    def test_create_category_target_url(self) -> None:
        self.assertEqual(self.url, '/create_target/category/1')

    def test_get_target_category_form(self) -> None:
        self._login(self.test_user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/create_targets.html')
        form: TargetForm = response.context['form']
        self.assertTrue(isinstance(form, TargetForm))
        self.assertFalse(form.is_bound)
        messages_list: list[Message] = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_invalid_pk_entered(self) -> None:
        self._login(self.test_user)
        url: str = reverse(
            "create_category_target", kwargs={
                "pk": 99999999})
        response: HttpResponse = self.client.get(url, follow=True)
        response_url: str = reverse("dashboard")
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, "pages/dashboard.html")

    def test_other_users_category_pk_entered(self) -> None:
        self._login(self.test_user)
        url: str = reverse(
            "create_category_target", kwargs={
                "pk": 3})
        response: HttpResponse = self.client.get(url, follow=True)
        response_url: str = reverse("dashboard")
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, "pages/dashboard.html")

    def test_successful_category_target_form_submission(self) -> None:
        self._login(self.test_user)
        before_count: int = CategoryTarget.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count: int = CategoryTarget.objects.count()
        self.assertEqual(after_count, before_count + 1)
        self.assertTemplateUsed(response, 'pages/individual_category.html')

    def test_invalid_category_target_form_submission(self) -> None:
        self._login(self.test_user)
        self.form_input['target_type']: str = ''
        before_count: int = CategoryTarget.objects.count()
        response: HttpResponse = self.client.post(self.url, self.form_input, follow=True)
        after_count: int = CategoryTarget.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertTemplateUsed(response, 'pages/create_targets.html')

    def test_unsuccessful_category_target_form_due_to_failing_unique_constraints(
            self) -> None:
        self.form_input: dict[str, Any] = {
            'target_type': self.test_category_target.target_type,
            'timespan': self.test_category_target.timespan,
            'amount': 200.00,
            'currency': 'USD'
        }
        self._login(self.test_user)
        before_count: int = CategoryTarget.objects.count()
        response: HttpResponse = self.client.post(self.url, self.form_input, follow=True)
        self.assertTemplateUsed(response, 'pages/create_targets.html')
        messages_list: list[Message] = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        after_count: int = CategoryTarget.objects.count()
        self.assertEqual(after_count, before_count)

    def test_get_view_redirects_when_not_logged_in(self) -> None:
        self._assert_require_login(self.url)
