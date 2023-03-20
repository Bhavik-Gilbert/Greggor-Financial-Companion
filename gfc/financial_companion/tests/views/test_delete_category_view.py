from django.urls import reverse
from .test_view_base import ViewTestCase
from financial_companion.models import User, Category
from django.http import HttpResponse
from django.contrib.messages.storage.base import Message


class DeleteCategoryViewTestCase(ViewTestCase):
    """Tests of the delete category view."""

    def setUp(self) -> None:
        self.url: str = reverse('delete_category', kwargs={"pk": 1})
        self.user: User = User.objects.get(username='@johndoe')

    def test_delete_category_url(self) -> None:
        self.assertEqual(self.url, '/delete_category/1')

    def test_successful_deletion(self) -> None:
        self._login(self.user)
        before_count: int = Category.objects.count()
        response: HttpResponse = self.client.get(self.url, follow=True)
        after_count: int = Category.objects.count()
        self.assertEqual(after_count + 1, before_count)
        self.assertTemplateUsed(response, 'pages/category_list.html')
        messages_list: list[Message] = list(response.context['messages'])
        self.assertEqual(len(messages_list), 2)

    def test_user_tries_to_delete_someone_elses_category(self):
        self._login(self.user)
        self.url: str = reverse('delete_category', kwargs={"pk": 3})
        response_url: str = reverse("dashboard")
        response: HttpResponse = self.client.get(self.url, follow=True)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, 'pages/dashboard.html')

    def test_user_provides_invalid_pk(self):
        self._login(self.user)
        self.url: str = reverse('delete_category', kwargs={"pk": 300})
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
