from django.contrib.auth.hashers import check_password
from django.urls import reverse

from .test_view_base import ViewTestCase
from financial_companion.forms import CategoryForm
from financial_companion.models import User, Category
from django.http import HttpRequest, HttpResponse


class EditCategoryViewTestCase(ViewTestCase):
    """Tests of the edit category view."""

    def setUp(self) -> None:
        self.url: str = reverse('edit_category', kwargs={"pk": 1})
        self.form_input: dict[str, str] = {
            'name': 'Travel',
            'description': 'Travel Expenses'
        }
        self.user: User = User.objects.get(username='@johndoe')

    def test_edit_category_url(self) -> None:
        self.assertEqual(self.url, '/edit_category/1')

    def test_get_edit_category(self) -> None:
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/create_category.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CategoryForm))
        self.assertFalse(form.is_bound)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_unsuccessful_edit_category_form_submission(self) -> None:
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.form_input['name'] = ''
        before_count: int = Category.objects.count()
        response: HttpResponse = self.client.post(self.url, self.form_input)
        after_count: int = Category.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/create_category.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CategoryForm))

    def test_successful_edit_category_form_submission(self) -> None:
        self._login(self.user)
        before_count: int = Category.objects.count()
        response: HttpResponse = self.client.post(self.url, self.form_input, follow=True)
        after_count: int = Category.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertTemplateUsed(response, 'pages/individual_category.html')

    def test_user_tries_to_edit_someone_elses_category(self) -> None:
        self._login(self.user)
        self.url: str = reverse('edit_category', kwargs={"pk": 3})
        response_url: str = reverse("dashboard")
        response: HttpResponse = self.client.post(self.url, self.form_input, follow=True)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, 'pages/dashboard.html')

    def test_user_provides_invalid_pk(self) -> None:
        self._login(self.user)
        self.url: str = reverse('edit_category', kwargs={"pk": 300})
        response_url: str = reverse("dashboard")
        response: HttpResponse = self.client.post(self.url, self.form_input, follow=True)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, 'pages/dashboard.html')

    def test_get_view_redirects_when_not_logged_in(self) -> None:
        self._assert_require_login(self.url)
