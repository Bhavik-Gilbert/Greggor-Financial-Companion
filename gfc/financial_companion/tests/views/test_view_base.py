from django.contrib import auth
from django.http import HttpResponse
from django.urls import reverse
from typing import Any

from ..test_base import BaseTestCase
from ...models import User


class ViewTestCase(BaseTestCase):
    """
    Base class for testing views.
    Call super().setUp() in the
    setUp() method of the subclass.
    """

    def _login(self, user: User, password: str = 'Password123') -> bool:
        """
        Logs given user in

        Return True if the user was logged in successfully.
        Otherwise, return False.
        """

        return self.client.login(username=user.username, password=password)

    def _is_logged_in(self) -> bool:
        """
        Return True if the user is logged in
        Otherwise, return False.
        """
        return '_auth_user_id' in self.client.session.keys()

    def _reverse_with_query(self, view: str, **kwargs) -> str:
        """
        Generate reverse URL with given query parameters
        """
        url: str = reverse(view)

        if len(kwargs):
            url += "?"

            first: bool = True
            for key in kwargs:
                if first:
                    first = False
                else:
                    url += "&"

                url += key + "=" + kwargs[key]

        return url

    def _assert_require_login(self, url: str) -> None:
        """Asserts users are not allowed to access this page when logged out"""
        user: User = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)
        response: HttpResponse = self.client.get(url, follow=True)
        expected_url: str = self._reverse_with_query("log_in", next=url)
        self.assertRedirects(
            response,
            expected_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, "pages/log_in.html")

    def _assert_require_logout(self, url: str) -> None:
        """Asserts users are not allowed to access this page when logged in"""
        user: User = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        response: HttpResponse = self.client.get(url, follow=True)
        redirect_url: str = reverse('dashboard')
        self.assertRedirects(
            response,
            redirect_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, "pages/dashboard.html")

    def _assert_response_contains(
            self, response: HttpResponse, contain_list: list[Any]):
        """Asserts the response contains the elements in the list"""
        for element in contain_list:
            self.assertContains(response, element)
