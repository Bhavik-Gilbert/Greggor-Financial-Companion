from django.urls import reverse
from .test_view_base import ViewTestCase
from financial_companion.models import User, UserTarget


class DeleteUserTargetViewTestCase(ViewTestCase):
    """Tests of the delete user target view."""

    def setUp(self):
        self.url = reverse('delete_user_target', kwargs={"pk": 1})
        self.user = User.objects.get(username='@johndoe')

    def test_delete_user_target_url(self):
        self.assertEqual(self.url, '/delete_target/user/1')

    def test_successful_deletion(self):
        self._login(self.user)
        before_count = UserTarget.objects.count()
        response = self.client.get(self.url, follow=True)
        after_count = UserTarget.objects.count()
        self.assertEqual(after_count + 1, before_count)
        self.assertTemplateUsed(response, 'pages/dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 2)
        self.assertTrue('Targets exceeded: ' in str(messages_list[1]))

    def test_user_tries_to_delete_someone_elses_user_target(self):
        self._login(self.user)
        self.url = reverse('delete_user_target', kwargs={"pk": 2})
        response_url: str = reverse("dashboard")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, 'pages/dashboard.html')

    def test_user_provides_invalid_pk(self):
        self._login(self.user)
        self.url = reverse('delete_user_target', kwargs={"pk": 300})
        response_url: str = reverse("dashboard")
        response = self.client.get(self.url, follow=True)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, 'pages/dashboard.html')

    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
