from .test_view_base import ViewTestCase
from financial_companion.models import User, Category
from django.http import HttpResponse
from django.urls import reverse


class IndividualCategoryRedirectViewTestCase(ViewTestCase):
    """Unit tests of the individual category redirect view"""

    def setUp(self):
        self.user: User = User.objects.get(username="@johndoe")
        self.category: Category = Category.objects.filter(user=self.user)[0]
        self.url: str = reverse(
            "individual_category_redirect", kwargs={
                "pk": self.category.id})

    def test_valid_individual_category_redirect_url(self):
        self.assertEqual(self.url, f"/individual_category/{self.category.id}/")

    def test_valid_get_individual_category_redirect(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url: str = reverse(
            "individual_category", kwargs={
                "pk": self.category.id, "filter_type": "all"})
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, "pages/individual_category.html")

    def test_invalid_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
