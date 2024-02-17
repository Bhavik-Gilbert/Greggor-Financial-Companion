from .test_view_base import ViewTestCase
from financial_companion.models import User
from django.urls import reverse
from django.http import HttpResponse
from typing import Any
from django.contrib.messages.storage.base import Message
from freezegun import freeze_time

class FilterTransactionsViewTestCase(ViewTestCase):
    """Unit tests of the filter transactions request view"""

    def setUp(self):
        super().setUp()
        self.url: str = reverse(
            "filter_transaction_request", kwargs={
                "redirect_name": "view_transactions"})
        self.user: User = User.objects.get(username="@johndoe")

    def test_filter_transaction_request_url(self):
        self.assertEqual(
            self.url,
            "/filter_transaction_request/view_transactions/")

    @freeze_time("2023-03-29 13:00:00")
    def test_post_when_all_button_is_clicked(self):
        self._login(self.user)
        self.form_data: dict[str, bool] = {
            "all": True
        }
        response_url: str = reverse(
            "view_transactions", kwargs={
                "filter_type": "all"})
        response: HttpResponse = self.client.post(self.url, self.form_data)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        response: HttpResponse = self.client.post(response_url)
        self.assertTemplateUsed(response, "pages/display_transactions.html")
        messages_list: list[Message] = list(response.context["messages"])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, "New Car")
        self.assertContains(response, 4)
        self.assertContains(response, 14999.99)
        self.assertContains(response, "New Bike")
        self.assertContains(response, 5)
        self.assertContains(response, 499.99)

    @freeze_time("2023-03-29 13:00:00")
    def test_post_when_sent_button_is_clicked(self):
        self._login(self.user)
        self.form_data: dict[str, bool] = {
            "sent": True
        }
        response_url: str = reverse(
            "view_transactions", kwargs={
                "filter_type": "sent"})
        response: HttpResponse = self.client.post(self.url, self.form_data)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        response: HttpResponse = self.client.post(response_url)
        self.assertTemplateUsed(response, "pages/display_transactions.html")
        messages_list: list[Message] = list(response.context["messages"])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, "New Car")
        self.assertContains(response, 4)
        self.assertContains(response, 14999.99)

    @freeze_time("2023-03-29 13:00:00")
    def test_post_when_received_button_is_clicked(self):
        self._login(self.user)
        self.form_data: dict[str, bool] = {
            "received": True
        }
        response_url: str = reverse(
            "view_transactions", kwargs={
                "filter_type": "received"})
        response: HttpResponse = self.client.post(self.url, self.form_data)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        response: HttpResponse = self.client.post(response_url)
        self.assertTemplateUsed(response, "pages/display_transactions.html")
        messages_list: list[Message] = list(response.context["messages"])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, "New Bike")
        self.assertContains(response, 5)
        self.assertContains(response, 499.99)

    @freeze_time("2023-03-29 13:00:00")
    def test_post_when_random_input_is_given(self):
        self._login(self.user)
        self.form_data: dict[str, bool] = {
            "other": True
        }
        response_url: str = reverse("dashboard")
        response: HttpResponse = self.client.post(self.url, self.form_data)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        response: HttpResponse = self.client.post(response_url)
        self.assertTemplateUsed(response, "pages/dashboard.html")
        messages_list: list[Message] = list(response.context["messages"])
        self.assertEqual(len(messages_list), 2)
        self.assertTrue('Targets completed: ' in str(messages_list[0]))
        self.assertTrue('Targets nearly exceeded: ' in str(messages_list[1]))

    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
