from django.urls import reverse
from .test_view_base import ViewTestCase
from financial_companion.models import User, UserGroup
from financial_companion.forms import UserLogInForm


class AllGroupsViewCase(ViewTestCase):
    """Tests of the user view all groups view."""

    def setUp(self):
        self.url = reverse('all_groups', kwargs={'search_name': "all"})
        self.user = User.objects.get(username='@johndoe')

    def test_log_in_url(self):
        self.assertEqual(self.url, '/groups/all/')

    def test_post_when_search_is_empty(self):
        self._login(self.user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/all_groups.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, "Saving Club")
        self.assertContains(response, "johndoe@example.org")
        self.assertContains(response, "Save with us")

    def test_post_when_full_group_name_is_applied(self):
        self._login(self.user)
        self.url = reverse('all_groups', kwargs={'search_name': "Saving Club"})
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/all_groups.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, "Saving Club")
        self.assertContains(response, "johndoe@example.org")
        self.assertContains(response, "Save with us")

    def test_post_when_partial_group_name_is_applied(self):
        self._login(self.user)
        self.url = reverse('all_groups', kwargs={'search_name': "a"})
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/all_groups.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, "Saving Club")
        self.assertContains(response, "Save with us")
        self.assertContains(response, "SavingsRUs".title())
        self.assertContains(response, "Fun savers")

    def test_post_when_incorrect_category_name_is_applied(self):
        self._login(self.user)
        self.url = reverse(
            'all_groups', kwargs={
                'search_name': "Spending Club"})
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/all_groups.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
        self.assertNotContains(response, "Saving Club")
        self.assertNotContains(response, "Save with us")
        self.assertNotContains(response, "SavingsRUs")
        self.assertNotContains(response, "Fun savers")
        self.assertContains(response, "You have no groups yet")

    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
