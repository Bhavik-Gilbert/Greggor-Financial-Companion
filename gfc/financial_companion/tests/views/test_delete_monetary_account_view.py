from django.urls import reverse
from .test_view_base import ViewTestCase
from financial_companion.models import User, Account
from django.http import HttpResponse
from django.contrib.messages.storage.base import Message


class DeleteMonetaryAccountViewTestCase(ViewTestCase):
    """Tests of the delete monetary account view."""

    def setUp(self) -> None:
        super().setUp()
        self.url: str = reverse('delete_monetary_account', kwargs={"pk": 5})
        self.user: User = User.objects.get(username='@johndoe')

    def test_delete_monetary_account_url(self) -> None:
        self.assertEqual(self.url, '/delete_monetary_account/5/')

    def test_succesful_deletion(self) -> None:
        self._login(self.user)
        before_count: int = Account.objects.count()
        response: HttpResponse = self.client.get(self.url, follow=True)
        after_count: int = Account.objects.count()
        self.assertEqual(after_count + 1, before_count)
        self.assertTemplateUsed(response, 'pages/view_accounts.html')
        messages_list: list[Message] = list(response.context['messages'])
        self.assertEqual(len(messages_list), 2)

    def test_user_tries_to_edit_someone_elses_monetary_account(self) -> None:
        self._login(self.user)
        self.url: str = reverse('delete_monetary_account', kwargs={"pk": 4})
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
        self.url: str = reverse('delete_monetary_account', kwargs={"pk": 300})
        response_url: str = reverse("dashboard")
        response: HttpResponse = self.client.get(self.url, follow=True)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, 'pages/dashboard.html')

    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
