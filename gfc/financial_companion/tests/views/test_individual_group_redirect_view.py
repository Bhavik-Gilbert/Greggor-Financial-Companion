from django.http import HttpResponse
from django.urls import reverse
from .test_view_base import ViewTestCase
from financial_companion.models import User, UserGroup


class IndividualGroupRedirectViewTestCase(ViewTestCase):
    """Unit tests of the individual group redirect view"""

    def setUp(self):
        self.owner = User.objects.get(username='@johndoe')
        self.member = User.objects.get(username='@janedoe')
        self.group = UserGroup.objects.get(id=3)
        self.url: str = reverse("individual_group_redirect", kwargs={
            "pk": self.group.id})

    def test_valid_individual_group_url(self):
        self.assertEqual(
            self.url,
            f"/individual_group/{self.group.id}/")
