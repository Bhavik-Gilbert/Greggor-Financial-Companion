from django.urls import reverse
from .test_view_base import ViewTestCase
from financial_companion.models import User, Category
from financial_companion.forms import UserLogInForm


class CategoryListViewCase(ViewTestCase):
    """Tests of the user view categories view."""

    def setUp(self):
        self.url = reverse('categories_list', kwargs={'search_name': "all"})
        self.user = User.objects.get(username='@johndoe')

    def test_log_in_url(self):
        self.assertEqual(self.url, '/categories/all/')

    def test_post_when_search_is_empty(self):
        self._login(self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/category_list.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, "Food")
        self.assertContains(response, "Eating out expenses")
        self.assertContains(response, "Travel")
        self.assertContains(response, "Going to and from uni")
        self.assertContains(response, 'Entertainment')
        self.assertContains(response, 'Going out and having fun')

    def test_post_when_full_category_name_is_applied(self):
        self._login(self.user)
        self.url = reverse('categories_list', kwargs={'search_name': "Food"})
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/category_list.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, 'Food')
        self.assertContains(response, "Eating out expenses")

    def test_post_when_partial_category_name_is_applied(self):
        self._login(self.user)
        self.url = reverse('categories_list', kwargs={'search_name': "e"})
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/category_list.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, "Travel")
        self.assertContains(response, "Going to and from uni")
        self.assertContains(response, 'Entertainment')
        self.assertContains(response, 'Going out and having fun')

    def test_post_when_incorrect_category_name_is_applied(self):
        self._login(self.user)
        self.url = reverse(
            'categories_list', kwargs={
                'search_name': "Shopping"})
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/category_list.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertNotContains(response, "Food")
        self.assertNotContains(response, "Eating out expenses")
        self.assertNotContains(response, "Travel")
        self.assertNotContains(response, "Going to and from uni")
        self.assertNotContains(response, 'Entertainment')
        self.assertNotContains(response, 'Going out and having fun')
        self.assertContains(response, "You have no categories yet")

    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
