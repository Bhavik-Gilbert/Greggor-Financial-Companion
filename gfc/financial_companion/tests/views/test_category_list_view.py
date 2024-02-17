from django.urls import reverse
from .test_view_base import ViewTestCase
from financial_companion.models import User
from django.contrib.messages.storage.base import Message
from django.http import HttpResponse
from freezegun import freeze_time


class CategoryListViewCase(ViewTestCase):
    """Tests of the user view categories view."""

    def setUp(self) -> None:
        super().setUp()
        self.url: str = reverse(
            'categories_list', kwargs={
                'search_name': "all"})
        self.redirect_url: str = reverse('categories_list_redirect')
        self.user: User = User.objects.get(username='@johndoe')

    def test_category_list_view_url(self) -> None:
        self.assertEqual(self.url, '/categories/all/')

    def test_valid_categories_list_redirect_url(self) -> None:
        self.assertEqual(self.redirect_url, "/categories/")

    @freeze_time("2023-03-29 13:00:00")
    def test_valid_get_categories_list_redirect(self) -> None:
        self._login(self.user)
        response: HttpResponse = self.client.post(self.redirect_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/category_list.html')
        messages_list: list[Message] = list(response.context['messages'])
        self.assertEqual(len(messages_list), 2)
        self.assertTrue('Targets completed: ' in str(messages_list[0]))
        self.assertTrue('Targets nearly exceeded: ' in str(messages_list[1]))
        self.assertContains(response, "Food")
        self.assertContains(response, "Eating out expenses")
        self.assertContains(response, "Travel")
        self.assertContains(response, "Going to and from uni")
        self.assertContains(response, 'Entertainment')
        self.assertContains(response, 'Going out and having fun')

    @freeze_time("2023-03-29 13:00:00")
    def test_post_when_search_is_empty(self) -> None:
        self._login(self.user)
        response: HttpResponse = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/category_list.html')
        messages_list: list[Message] = list(response.context['messages'])
        self.assertEqual(len(messages_list), 2)
        self.assertTrue('Targets completed: ' in str(messages_list[0]))
        self.assertTrue('Targets nearly exceeded: ' in str(messages_list[1]))
        self.assertContains(response, "Food")
        self.assertContains(response, "Eating out expenses")
        self.assertContains(response, "Travel")
        self.assertContains(response, "Going to and from uni")
        self.assertContains(response, 'Entertainment')
        self.assertContains(response, 'Going out and having fun')

    @freeze_time("2023-03-29 13:00:00")
    def test_post_when_full_category_name_is_applied(self) -> None:
        self._login(self.user)
        self.url: str = reverse(
            'categories_list', kwargs={
                'search_name': "Food"})
        response: HttpResponse = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/category_list.html')
        messages_list: list[Message] = list(response.context['messages'])
        self.assertTrue('Targets completed: ' in str(messages_list[0]))
        self.assertTrue('Targets nearly exceeded: ' in str(messages_list[1]))
        self.assertEqual(len(messages_list), 2)
        self.assertContains(response, 'Food')
        self.assertContains(response, "Eating out expenses")

    @freeze_time("2023-03-29 13:00:00")
    def test_post_when_partial_category_name_is_applied(self) -> None:
        self._login(self.user)
        self.url: str = reverse('categories_list', kwargs={'search_name': "e"})
        response: HttpResponse = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/category_list.html')
        messages_list: list[Message] = list(response.context['messages'])
        self.assertTrue('Targets completed: ' in str(messages_list[0]))
        self.assertTrue('Targets nearly exceeded: ' in str(messages_list[1]))
        self.assertEqual(len(messages_list), 2)
        self.assertContains(response, "Travel")
        self.assertContains(response, "Going to and from uni")
        self.assertContains(response, 'Entertainment')
        self.assertContains(response, 'Going out and having fun')

    @freeze_time("2023-03-29 13:00:00")
    def test_post_when_incorrect_category_name_is_applied(self):
        self._login(self.user)
        self.url = reverse(
            'categories_list', kwargs={
                'search_name': "Shopping"})
        response: HttpResponse = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/category_list.html')
        messages_list: list[Message] = list(response.context['messages'])
        self.assertTrue('Targets completed: ' in str(messages_list[0]))
        self.assertTrue('Targets nearly exceeded: ' in str(messages_list[1]))
        self.assertEqual(len(messages_list), 2)
        # "Food" is found in warning messages
        self.assertContains(response, "Food")
        self.assertNotContains(response, "Eating out expenses")
        self.assertNotContains(response, "Travel")
        self.assertNotContains(response, "Going to and from uni")
        # "Entertainment" is found in warning messages
        self.assertContains(response, 'Entertainment')
        self.assertNotContains(response, 'Going out and having fun')
        self.assertContains(response, "You have no categories yet")

    def test_view_redirects_when_search_button_pressed_for_valid_search_name(
            self) -> None:
        self.form_data: dict[str, bool] = {
            'search': True
        }
        self._login(self.user)
        self.url: str = reverse(
            'categories_list', kwargs={
                'search_name': "Food"})
        response: HttpResponse = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 302)

    def test_view_redirects_when_search_button_pressed_for_invalid_search_name(
            self) -> None:
        self.form_data: dict[str, str] = {
            'search': ""
        }
        self._login(self.user)
        self.url: str = reverse(
            'categories_list', kwargs={
                'search_name': None})
        response: HttpResponse = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 302)

    def test_get_view_redirects_when_not_logged_in(self) -> None:
        self._assert_require_login(self.url)
