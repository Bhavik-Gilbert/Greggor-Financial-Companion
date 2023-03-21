from django.urls import reverse
from django.http import HttpResponse
from .test_view_base import ViewTestCase
from financial_companion.helpers import GreggorTypes
from financial_companion.models import User


class HomeViewTestCase(ViewTestCase):
    """Unit tests of the home view"""

    def setUp(self):
        self.url: str = reverse('home')
        self.user: User = User.objects.get(username='@johndoe')

    def test_valid_home_url(self):
        self.assertEqual(self.url, '/')

    def test_valid_get_home(self):
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/index.html')
        logo_types: GreggorTypes = response.context['logo_types']
        self.assertTrue(isinstance(logo_type, GreggorTypes)
                        for logo_type in logo_types)

    def test_valid_get_home_page_redirects_when_logged_in(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url, follow=True)
        self._assert_require_logout(self.url)
