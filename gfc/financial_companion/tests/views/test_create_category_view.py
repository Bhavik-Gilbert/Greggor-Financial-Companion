from django.contrib.auth.hashers import check_password
from django.urls import reverse

from .test_view_base import ViewTestCase
from financial_companion.forms import CategoryForm
from financial_companion.models import User, Category
from django.http import HttpResponse
from typing import Any
from django.contrib.messages.storage.base import Message


class CreateCategoryViewTestCase(ViewTestCase):
    """Tests of the create category view."""

    def setUp(self) -> None:
        self.url: str = reverse('create_category')
        self.form_input: dict[str, str] = {
            'name': 'Travel',
            'description': 'Travel Expenses'
        }
        self.user: User = User.objects.get(username='@johndoe')

    def test_create_category_url(self) -> None:
        self.assertEqual(self.url, '/create_category/')

    def test_get_create_category(self) -> None:
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/create_category.html')
        form: CategoryForm = response.context['form']
        self.assertTrue(isinstance(form, CategoryForm))
        self.assertFalse(form.is_bound)
        messages_list: list[Message] = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_unsuccessful_create_category_form_submission(self) -> None:
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.form_input['name']: str = ''
        before_count: int = Category.objects.count()
        response: HttpResponse = self.client.post(self.url, self.form_input)
        after_count: int = Category.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/create_category.html')
        form: CategoryForm = response.context['form']
        self.assertTrue(isinstance(form, CategoryForm))

    def test_successful_category_form_submission(self) -> None:
        self._login(self.user)
        before_count: int = Category.objects.count()
        response: HttpResponse = self.client.post(
            self.url, self.form_input, follow=True)
        after_count: int = Category.objects.count()
        self.assertEqual(after_count, before_count + 1)
        self.assertTemplateUsed(response, 'pages/category_list.html')
        response_url: str = reverse(
            "categories_list", kwargs={
                'search_name': "all"})
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)

    def test_get_view_redirects_when_not_logged_in(self) -> None:
        self._assert_require_login(self.url)
