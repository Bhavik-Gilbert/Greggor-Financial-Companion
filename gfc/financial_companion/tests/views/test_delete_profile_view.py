from .test_view_base import ViewTestCase
from financial_companion.models import User
from django.urls import reverse


class DeleteProfileViewTestCase(ViewTestCase):
    """Unit tests of the delete profile view"""

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('delete_profile')

    def test_delete_profile_url(self):
        self.assertEqual(self.url, '/delete_profile/')

    def test_get_delete_profile(self):
        self._login(self.user)
        before_count = User.objects.count()
        response = self.client.get(self.url)
        after_count = User.objects.count()
        self.assertEqual(before_count - 1, after_count)
        response_url = reverse('home')
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
