from .test_view_base import ViewTestCase
from financial_companion.models import User
from django.urls import reverse


class ProfileViewTestCase(ViewTestCase):
    """Unit tests of the profile view"""

    def setUp(self):
        self.url: str = reverse('profile')
        self.user: User = User.objects.get(username='@michaelkolling')

    def test_profile_url(self):
        self.assertEqual(self.url, '/profile/')

    def test_get_profile(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/profile.html')
        self.assertContains(response, "Profile")
        self.assertContains(response, self.user)
        self.assertContains(response, self.user.profile_picture)
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.user.first_name)
        self.assertContains(response, self.user.last_name)
        self.assertContains(response, self.user.email)
        self.assertContains(response, self.user.bio)

    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
