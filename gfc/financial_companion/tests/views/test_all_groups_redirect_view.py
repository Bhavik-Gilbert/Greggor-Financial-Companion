from .test_view_base import ViewTestCase
from financial_companion.models import User
from django.http import HttpResponse
from django.urls import reverse


class AllGroupsRedirectViewTestCase(ViewTestCase):
    """Unit tests of the view all groups redirect view"""

    def setUp(self):
        self.user: User = User.objects.get(username="@johndoe")
        self.url: str = reverse("all_groups_redirect")

    def test_valid_all_groups_redirect_url(self):
        self.assertEqual(self.url, "/groups/")

    def test_valid_get_all_groups_redirect(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url: str = reverse(
            "all_groups", kwargs={
                "search_name": "all"})
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, "pages/all_groups.html")

    def test_invalid_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
