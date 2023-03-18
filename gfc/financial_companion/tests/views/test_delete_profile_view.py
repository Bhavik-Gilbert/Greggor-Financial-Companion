from .test_view_base import ViewTestCase
from financial_companion.models import User
from django.urls import reverse
from django.http import HttpRequest, HttpResponse


class DeleteProfileViewTestCase(ViewTestCase):
    """Unit tests of the delete profile view"""

    def setUp(self) -> None:
        self.user: User = User.objects.get(username='@johndoe')
        self.url: str = reverse('delete_profile')

    def test_delete_profile_url(self) -> None:
        self.assertEqual(self.url, '/delete_profile/')

    def test_get_delete_profile(self):
        self._login(self.user)
        before_count: int = User.objects.count()
        response: HttpResponse = self.client.get(self.url)
        after_count: int = User.objects.count()
        self.assertEqual(before_count - 1, after_count)
        response_url: str = reverse('home')
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
