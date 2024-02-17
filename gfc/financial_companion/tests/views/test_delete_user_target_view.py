from django.urls import reverse
from .test_view_base import ViewTestCase
from financial_companion.models import User, UserTarget
from django.http import HttpResponse
from django.contrib.messages.storage.base import Message
from freezegun import freeze_time


class DeleteUserTargetViewTestCase(ViewTestCase):
    """Tests of the delete user target view."""

    def setUp(self) -> None:
        super().setUp()
        self.url: str = reverse('delete_user_target', kwargs={"pk": 1})
        self.user: User = User.objects.get(username='@johndoe')

    def test_delete_user_target_url(self) -> None:
        self.assertEqual(self.url, '/delete_target/user/1')

    @freeze_time("2023-03-29 13:00:00")
    def test_successful_deletion(self) -> None:
        self._login(self.user)
        before_count: int = UserTarget.objects.count()
        response: HttpResponse = self.client.get(self.url, follow=True)
        after_count: int = UserTarget.objects.count()
        self.assertEqual(after_count + 1, before_count)
        self.assertTemplateUsed(response, 'pages/dashboard.html')
        messages_list: list[Message] = list(response.context['messages'])
        self.assertEqual(len(messages_list), 3)
        self.assertTrue(
            'This user target has been deleted' in str(
                messages_list[0]))
        self.assertTrue('Targets completed: ' in str(messages_list[1]))
        self.assertTrue('Targets nearly exceeded: ' in str(messages_list[2]))

    def test_user_tries_to_delete_someone_elses_user_target(self) -> None:
        self._login(self.user)
        self.url: str = reverse('delete_user_target', kwargs={"pk": 2})
        response_url: str = reverse("dashboard")
        response: HttpResponse = self.client.get(self.url, follow=True)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, 'pages/dashboard.html')

    def test_user_provides_invalid_pk(self) -> None:
        self._login(self.user)
        self.url: str = reverse('delete_user_target', kwargs={"pk": 300})
        response_url: str = reverse("dashboard")
        response: HttpResponse = self.client.get(self.url, follow=True)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, 'pages/dashboard.html')

    def test_get_view_redirects_when_not_logged_in(self) -> None:
        self._assert_require_login(self.url)
