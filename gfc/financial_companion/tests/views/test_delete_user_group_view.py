from django.contrib.auth.hashers import check_password
from django.urls import reverse

from .test_view_base import ViewTestCase
from financial_companion.models import User, UserGroup
from django.http import HttpRequest, HttpResponse
from django.contrib.messages.storage.base import Message


class DeleteUserGroupViewTestCase(ViewTestCase):
    """Tests of the delete user group view."""

    def setUp(self) -> None:
        self.url: str = reverse('delete_user_group', kwargs={"pk": 1})
        self.user = User.objects.get(username='@johndoe')

    def test_delete_user_group_url(self) -> None:
        self.assertEqual(self.url, '/delete_user_group/1')

    def test_successful_deletion(self) -> None:
        self._login(self.user)
        before_count: int = UserGroup.objects.count()
        response: HttpResponse = self.client.get(self.url, follow=True)
        after_count: int = UserGroup.objects.count()
        self.assertEqual(after_count + 1, before_count)
        self.assertTemplateUsed(response, 'pages/all_groups.html')
        messages_list: list[Message] = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_user_tries_to_delete_group_as_a_non_owner(self) -> None:
        self._login(self.user)
        self.url: str = reverse('delete_user_group', kwargs={"pk": 2})
        response_url: str = reverse(
            "all_groups_redirect")
        before_count: int = UserGroup.objects.count()
        response: HttpResponse = self.client.get(self.url, follow=True)
        after_count: int = UserGroup.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, 'pages/all_groups.html')

    def test_user_provides_invalid_pk(self) -> None:
        self._login(self.user)
        self.url: str = reverse('delete_user_group', kwargs={"pk": 300})
        response_url: str = reverse(
            "all_groups_redirect")
        before_count: int = UserGroup.objects.count()
        response: HttpResponse = self.client.get(self.url, follow=True)
        after_count: int = UserGroup.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, 'pages/all_groups.html')

    def test_get_view_redirects_when_not_logged_in(self) -> None:
        self._assert_require_login(self.url)
