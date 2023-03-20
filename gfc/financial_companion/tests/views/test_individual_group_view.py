from django.http import HttpResponse
from django.urls import reverse
from .test_view_base import ViewTestCase
from financial_companion.models import User, UserGroup


class IndividualGroupViewTestCase(ViewTestCase):
    """Unit tests of the individual group view"""

    def setUp(self):
        self.owner = User.objects.get(username='@johndoe')
        self.member = User.objects.get(username='@janedoe')
        self.group = UserGroup.objects.get(id=3)
        self.url: str = reverse(
            "individual_group", kwargs={
                "pk": self.group.id, "leaderboard": "False"})
        self.redirect_url: str = reverse("individual_group_redirect", kwargs={
            "pk": self.group.id})

    def test_valid_individual_group_url(self):
        self.assertEqual(
            self.url,
            f"/individual_group/{self.group.id}/False/")

    def test_valid_individual_group_redirect_url(self):
        self.assertEqual(
            self.redirect_url,
            f"/individual_group/{self.group.id}/")

    def test_valid_get_view_individual_group_redirect(self):
        self._login(self.owner)
        response: HttpResponse = self.client.get(self.redirect_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/individual_group.html")
        group: UserGroup = response.context["group"]
        self.assertTrue(isinstance(group, UserGroup))
        self.assertContains(response, self.group.name)
        self.assertContains(response, self.group.invite_code)
        self.assertContains(response, self.group.description)
        self.assertContains(response, self.group.members_count())
        self.assertContains(response, self.group.owner_email)
        self.assertContains(response, "Members:")
        self.assertNotContains(response, "Leaderboard:")

    def test_valid_get_view_individual_group_with_members(self):
        self._login(self.owner)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/individual_group.html")
        group: UserGroup = response.context["group"]
        self.assertTrue(isinstance(group, UserGroup))
        self.assertContains(response, self.group.name)
        self.assertContains(response, self.group.invite_code)
        self.assertContains(response, self.group.description)
        self.assertContains(response, self.group.members_count())
        self.assertContains(response, self.group.owner_email)
        self.assertContains(response, "Members:")
        self.assertNotContains(response, "Leaderboard:")

    def test_valid_get_view_individual_group_with_leaderboard(self):
        self._login(self.owner)
        url: str = reverse(
            "individual_group", kwargs={
                "pk": self.group.id, "leaderboard": "True"})
        response: HttpResponse = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/individual_group.html")
        group: UserGroup = response.context["group"]
        self.assertTrue(isinstance(group, UserGroup))
        self.assertContains(response, self.group.name)
        self.assertContains(response, self.group.invite_code)
        self.assertContains(response, self.group.description)
        self.assertContains(response, self.group.members_count())
        self.assertContains(response, self.group.owner_email)
        self.assertContains(response, "Leaderboard:")
        self.assertContains(response, "1st")
        self.assertContains(response, "2nd")
        self.assertContains(response, ("For every income target which is completed you will gain one point." +
                                       " For every expense target completed you will lose a point." +
                                       " For every income target nearly completed (this is when it >= 75% completed and < 100% completed) you will gain half a point." +
                                       " For every expense target nearly completed you will lose half a point."))
        self.assertNotContains(response, "Members:")

    def test_invalid_group_does_not_exist(self):
        self._login(self.owner)
        url: str = reverse(
            "individual_group", kwargs={
                "pk": self.group.id + 99999999, "leaderboard": "False"})
        response: HttpResponse = self.client.get(url, follow=True)
        response_url: str = reverse("dashboard")
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, "pages/dashboard.html")

    def test_valid_get_view_individual_group_when_logged_in_as_owner(self):
        self._login(self.owner)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/individual_group.html")
        group: UserGroup = response.context["group"]
        self.assertTrue(isinstance(group, UserGroup))
        self.assertContains(response, self.group.name)
        self.assertContains(response, self.group.invite_code)
        self.assertContains(response, self.group.description)
        self.assertContains(response, self.group.members_count())
        self.assertContains(response, self.group.owner_email)
        self.assertContains(response, "User ID")
        self.assertContains(response, self.owner.id)
        self.assertContains(response, self.member.id)
        self.assertContains(response, "Name")
        self.assertContains(response, self.owner.full_name())
        self.assertContains(response, self.member.full_name())
        self.assertContains(response, "Username")
        self.assertContains(response, self.owner.username)
        self.assertContains(response, self.member.username)
        self.assertContains(response, "Action")

    def test_valid_get_view_individual_group_when_logged_in_as_member(self):
        self._login(self.member)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/individual_group.html")
        group: UserGroup = response.context["group"]
        self.assertTrue(isinstance(group, UserGroup))
        self.assertContains(response, self.group.name)
        self.assertContains(response, self.group.invite_code)
        self.assertContains(response, self.group.description)
        self.assertContains(response, self.group.members_count())
        self.assertContains(response, self.group.owner_email)
        self.assertContains(response, "User ID")
        self.assertContains(response, self.owner.id)
        self.assertContains(response, self.member.id)
        self.assertContains(response, "Name")
        self.assertContains(response, self.owner.full_name())
        self.assertContains(response, self.member.full_name())
        self.assertContains(response, "Username")
        self.assertContains(response, self.owner.username)
        self.assertContains(response, self.member.username)
        self.assertNotContains(response, "Action")

    def test_invalid_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
