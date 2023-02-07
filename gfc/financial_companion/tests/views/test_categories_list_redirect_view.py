from .test_view_base import ViewTestCase
from financial_companion.models import User
from django.http import HttpResponse
from django.urls import reverse


class CategoriesListRedirectViewTestCase(ViewTestCase):
    """Unit tests of the categories list redirect view"""

    def setUp(self):
        self.user: User = User.objects.get(username="@johndoe")
        self.url: str = reverse("categories_list_redirect")

    def test_valid_categories_list_redirect_url(self):
        self.assertEqual(self.url, "/categories/")

    def test_valid_get_categories_list_redirect(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url: str = reverse(
            "categories_list", kwargs={
                "search_name": "all"})
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, "pages/category_list.html")

    def test_invalid_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
