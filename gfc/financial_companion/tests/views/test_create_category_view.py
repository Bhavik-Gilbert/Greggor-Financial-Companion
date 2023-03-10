from django.contrib.auth.hashers import check_password
from django.urls import reverse

from .test_view_base import ViewTestCase
from financial_companion.forms import CategoryForm
from financial_companion.models import User, Category


class CreateCategoryViewTestCase(ViewTestCase):
    """Tests of the create category view."""

    def setUp(self):
        self.url = reverse('create_category')
        self.form_input = {
            'name': 'Travel',
            'description': 'Travel Expenses'
        }
        self.user = User.objects.get(username='@johndoe')

    def test_create_category_url(self):
        self.assertEqual(self.url, '/create_category/')

    def test_get_create_category(self):
        self._login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/create_category.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CategoryForm))
        self.assertFalse(form.is_bound)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_unsuccessful_create_category_form_submission(self):
        self._login(self.user)
        response = self.client.get(self.url)
        self.form_input['name'] = ''
        before_count = Category.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Category.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/create_category.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CategoryForm))

    def test_successful_category_form_submission(self):
        self._login(self.user)
        before_count = Category.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Category.objects.count()
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

    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
