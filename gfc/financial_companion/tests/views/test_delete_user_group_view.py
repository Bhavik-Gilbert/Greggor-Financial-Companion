from django.contrib.auth.hashers import check_password
from django.urls import reverse

from .test_view_base import ViewTestCase
from financial_companion.models import User, UserGroup


class DeleteUserGroupViewTestCase(ViewTestCase):
    """Tests of the delete user group view."""

    def setUp(self):
        self.url = reverse('delete_user_group', kwargs={"pk": 1})
        self.user = User.objects.get(username='@johndoe')

    def test_delete_user_group_url(self):
        self.assertEqual(self.url, '/delete_user_group/1')

    def test_successful_deletion(self):
        self._login(self.user)
        before_count = UserGroup.objects.count()
        response = self.client.get(self.url, follow=True)
        after_count = UserGroup.objects.count()
        self.assertEqual(after_count + 1, before_count)
        self.assertTemplateUsed(response, 'pages/all_groups.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_user_tries_to_delete_group_as_a_non_owner(self):
        self._login(self.user)
        self.url = reverse('delete_user_group', kwargs={"pk": 2})
        response_url: str = reverse(
            "all_groups", kwargs={
                "search_name": "all"})
        before_count = UserGroup.objects.count()
        response = self.client.get(self.url, follow=True)
        after_count = UserGroup.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, 'pages/all_groups.html')

    def test_user_provides_invalid_pk(self):
        self._login(self.user)
        self.url = reverse('delete_user_group', kwargs={"pk": 300})
        response_url: str = reverse(
            "all_groups", kwargs={
                "search_name": "all"})
        before_count = UserGroup.objects.count()
        response = self.client.get(self.url, follow=True)
        after_count = UserGroup.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, 'pages/all_groups.html')

    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
