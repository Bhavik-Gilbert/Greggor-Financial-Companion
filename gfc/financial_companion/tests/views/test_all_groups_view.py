from django.urls import reverse
from .test_view_base import ViewTestCase
from financial_companion.models import User
from django.http import HttpResponse
from django.contrib.messages.storage.base import Message


class AllGroupsViewCase(ViewTestCase):
    """Tests of the user view all groups view."""

    def setUp(self) -> None:
        super().setUp()
        self.url: str = reverse('all_groups', kwargs={'search_name': "all"})
        self.redirect_url: str = reverse('all_groups_redirect')
        self.user: User = User.objects.get(username='@johndoe')

    def test_view_all_groups_url(self) -> None:
        self.assertEqual(self.url, '/groups/all/')

    def test_post_when_search_is_empty(self) -> None:
        self._login(self.user)
        response: HttpResponse = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/all_groups.html')
        messages_list: list[Message] = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, "Saving Club")
        self.assertContains(response, "johndoe@example.org")
        self.assertContains(response, "Save with us")

    def test_valid_all_groups_redirect_url(self) -> None:
        self.assertEqual(self.redirect_url, "/groups/")

    def test_valid_get_all_groups_redirect(self) -> None:
        self._login(self.user)
        response: HttpResponse = self.client.post(self.redirect_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/all_groups.html')
        messages_list: list[Message] = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, "Saving Club")
        self.assertContains(response, "johndoe@example.org")
        self.assertContains(response, "Save with us")

    def test_post_when_full_group_name_is_applied(self) -> None:
        self._login(self.user)
        self.url: str = reverse(
            'all_groups', kwargs={
                'search_name': "Saving Club"})
        response: HttpResponse = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/all_groups.html')
        messages_list: list[Message] = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, "Saving Club")
        self.assertContains(response, "johndoe@example.org")
        self.assertContains(response, "Save with us")

    def test_post_when_partial_group_name_is_applied(self) -> None:
        self._login(self.user)
        self.url: str = reverse('all_groups', kwargs={'search_name': "a"})
        response: HttpResponse = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/all_groups.html')
        messages_list: list[Message] = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, "Saving Club")
        self.assertContains(response, "Save with us")
        self.assertContains(response, "SavingsRUs")
        self.assertContains(response, "Fun savers")

    def test_post_when_incorrect_group_name_is_applied(self) -> None:
        self._login(self.user)
        self.url: str = reverse(
            'all_groups', kwargs={
                'search_name': "Spending Club"})
        response: HttpResponse = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/all_groups.html')
        messages_list: list[Message] = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertNotContains(response, "Saving Club")
        self.assertNotContains(response, "Save with us")
        self.assertNotContains(response, "SavingsRUs")
        self.assertNotContains(response, "Fun savers")
        self.assertContains(response, "You have no groups yet")

    def test_view_redirects_when_search_button_pressed_for_valid_search_name(
            self) -> None:
        self.form_data: dict[str, bool] = {
            'search': True
        }
        self._login(self.user)
        self.url: str = reverse(
            'all_groups', kwargs={
                'search_name': "Spending Club"})
        response: HttpResponse = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 302)

    def test_view_redirects_when_search_button_pressed_for_invalid_search_name(
            self) -> None:
        self.form_data: dict[str, str] = {
            'search': ""
        }
        self._login(self.user)
        self.url: str = reverse(
            'all_groups', kwargs={
                'search_name': None})
        response: HttpResponse = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 302)

    def test_get_view_redirects_when_not_logged_in(self) -> None:
        self._assert_require_login(self.url)
