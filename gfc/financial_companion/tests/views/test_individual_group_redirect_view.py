from django.http import HttpResponse
from django.urls import reverse
from .test_view_base import ViewTestCase
from financial_companion.models import User, UserGroup


class IndividualGroupRedirectViewTestCase(ViewTestCase):
    """Unit tests of the individual group redirect view"""

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.group = UserGroup.objects.get(id=3)
        self.url: str = reverse("individual_group_redirect", kwargs={
            "pk": self.group.id})

    def test_valid_individual_group_redirect_url(self):
        self.assertEqual(self.url, f"/individual_group/{self.group.id}/")

    def test_valid_get_view_individual_group_redirect(self):
        self._login(self.user)
        response = self.client.get(self.url, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse(
            'individual_group', kwargs={
                'pk': self.group.id, 'leaderboard': 'False'})
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, 'pages/individual_group.html')

    def test_invalid_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
