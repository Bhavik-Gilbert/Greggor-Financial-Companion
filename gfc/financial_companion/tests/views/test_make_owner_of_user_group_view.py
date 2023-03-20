from django.urls import reverse

from .test_view_base import ViewTestCase
from financial_companion.models import User, UserGroup
from django.contrib.messages.storage.base import Message


class MakeUserOwnerOfGroupViewTestCase(ViewTestCase):
    """Tests for make user owner of user group view."""

    def setUp(self):
        self.url: str = reverse(
            'make_owner_of_user_group', kwargs={
                "group_pk": 1, "user_pk": 2})
        self.user: User = User.objects.get(username='@johndoe')
        self.user_two: User = User.objects.get(username='@janedoe')
        self.user_group: UserGroup = UserGroup.objects.get(
            invite_code="ABCDEFGH")
        self.user_group.add_member(self.user)
        self.user_group.add_member(self.user_two)

    def test_make_user_owner_of_user_group_url(self):
        self.assertEqual(self.url, '/make_owner_of_user_group/1/2')

    def test_successful_make_user_owner_of_user_group(self):
        self._login(self.user)
        self.assertEqual(self.user_group.owner_email, self.user.email)
        before_owner_email: str = self.user_group.owner_email
        response: HttpResponse = self.client.get(self.url, follow=True)
        self.user_group.refresh_from_db()
        after_owner_email: str = self.user_group.owner_email
        self.assertNotEqual(before_owner_email, after_owner_email)
        self.assertNotEqual(self.user_group.owner_email, self.user.email)
        self.assertEqual(self.user_group.owner_email, self.user_two.email)
        self.assertTemplateUsed(response, 'pages/individual_group.html')
        messages_list: list[Message] = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_unsuccessful_make_user_owner_of_user_group_due_to_invalid_group_pk(
            self):
        self._login(self.user)
        url: str = reverse(
            'make_owner_of_user_group',
            kwargs={
                "group_pk": 1000,
                "user_pk": 2})
        self.assertEqual(self.user_group.owner_email, self.user.email)
        before_owner_email: str = self.user_group.owner_email
        response: HttpResponse = self.client.get(url, follow=True)
        self.user_group.refresh_from_db()
        after_owner_email: str = self.user_group.owner_email
        self.assertEqual(before_owner_email, after_owner_email)
        self.assertEqual(self.user_group.owner_email, self.user.email)
        self.assertTemplateUsed(response, 'pages/all_groups.html')
        messages_list: list[Message] = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_unsuccessful_make_user_owner_of_user_group_due_to_invalid_user_pk(
            self):
        self._login(self.user)
        url: str = reverse(
            'make_owner_of_user_group',
            kwargs={
                "group_pk": 1,
                "user_pk": 1000})
        self.assertEqual(self.user_group.owner_email, self.user.email)
        before_owner_email: str = self.user_group.owner_email
        response: HttpResponse = self.client.get(url, follow=True)
        self.user_group.refresh_from_db()
        after_owner_email: str = self.user_group.owner_email
        self.assertEqual(before_owner_email, after_owner_email)
        self.assertEqual(self.user_group.owner_email, self.user.email)
        self.assertTemplateUsed(response, 'pages/individual_group.html')
        messages_list: list[Message] = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_unsuccessful_make_user_owner_of_user_group_due_to_user_not_being_a_member_of_user_group(
            self):
        self._login(self.user)
        self.user_group.remove_member(self.user_two)
        self.assertEqual(self.user_group.owner_email, self.user.email)
        before_owner_email: str = self.user_group.owner_email
        response: HttpResponse = self.client.get(self.url, follow=True)
        self.user_group.refresh_from_db()
        after_owner_email: str = self.user_group.owner_email
        self.assertEqual(before_owner_email, after_owner_email)
        self.assertEqual(self.user_group.owner_email, self.user.email)
        self.assertTemplateUsed(response, 'pages/individual_group.html')
        messages_list: list[Message] = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)

    def test_unsuccessful_make_user_owner_of_user_group_due_to_request_user_not_being_the_owner_of_user_group(
            self):
        self._login(self.user_two)
        self.assertEqual(self.user_group.owner_email, self.user.email)
        before_owner_email: str = self.user_group.owner_email
        response: HttpResponse = self.client.get(self.url, follow=True)
        self.user_group.refresh_from_db()
        after_owner_email: str = self.user_group.owner_email
        self.assertEqual(before_owner_email, after_owner_email)
        self.assertEqual(self.user_group.owner_email, self.user.email)
        self.assertTemplateUsed(response, 'pages/all_groups.html')
        messages_list: list[Message] = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
