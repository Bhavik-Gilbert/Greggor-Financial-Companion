from django.urls import reverse
from .test_view_base import ViewTestCase
from financial_companion.models import User, Category

class ViewAccountsViewTestCase(ViewTestCase):
    """Tests of the user view categories view."""

    def setUp(self):
        self.url = reverse('categories_list')
        self.user = User.objects.get(username='@johndoe')
        self.categories = Category.objects.filter(user=self.user)

    def test_view_accounts_url(self):
        self.assertEqual(self.url,'/categories/')

    def test_get_view_categories(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/category_list.html')

    def test_get_view_categories_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)

    def test_view_accounts_contains_accounts_by_self(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertContains(response, self.categories[0].id)
