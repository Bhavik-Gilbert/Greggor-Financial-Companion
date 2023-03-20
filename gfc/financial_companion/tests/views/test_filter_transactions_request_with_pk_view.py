from .test_view_base import ViewTestCase
from financial_companion.models import User, PotAccount
from django.urls import reverse


class FilterTransactionsWithPKViewTestCase(ViewTestCase):
    """Unit tests of the filter transactions request with pk view"""

    def setUp(self):
        self.user: User = User.objects.get(username="@johndoe")
        self.account: PotAccount = PotAccount.objects.filter(user=self.user)[0]
        self.url = reverse(
            "filter_transaction_request_with_pk", kwargs={
                "redirect_name": "individual_account",
                "pk": self.account.id
            })

    def test_filter_transaction_request_with_pk_url(self):
        self.assertEqual(
            self.url,
            f"/filter_transaction_request_with_pk/individual_account/{self.account.id}/")

    def test_post_when_all_button_is_clicked(self):
        self._login(self.user)
        self.form_data = {
            "all": True
        }
        response_url = reverse(
            "individual_account", kwargs={
                "pk": self.account.id,
                "filter_type": "all"
            })
        response = self.client.post(self.url, self.form_data)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        response = self.client.post(response_url)
        self.assertTemplateUsed(response, "pages/individual_account.html")
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, "New Car")
        self.assertContains(response, 4)
        self.assertContains(response, 14999.99)
        self.assertContains(response, "New Bike")
        self.assertContains(response, 5)
        self.assertContains(response, 499.99)

    def test_post_when_sent_button_is_clicked(self):
        self._login(self.user)
        self.form_data = {
            "sent": True
        }
        response_url = reverse(
            "individual_account", kwargs={
                "pk": self.account.id,
                "filter_type": "sent"
            })
        response = self.client.post(self.url, self.form_data)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        response = self.client.post(response_url)
        self.assertTemplateUsed(response, "pages/individual_account.html")
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, "New Car")
        self.assertContains(response, 4)
        self.assertContains(response, 14999.99)

    def test_post_when_received_button_is_clicked(self):
        self._login(self.user)
        self.form_data = {
            "received": True
        }
        response_url = reverse(
            "individual_account", kwargs={
                "pk": self.account.id,
                "filter_type": "received"
            })
        response = self.client.post(self.url, self.form_data)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        response = self.client.post(response_url)
        self.assertTemplateUsed(response, "pages/individual_account.html")
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 0)
        self.assertContains(response, "New Bike")
        self.assertContains(response, 5)
        self.assertContains(response, 499.99)

    def test_post_when_random_input_is_given(self):
        self._login(self.user)
        self.form_data = {
            "other": True
        }
        response_url = reverse("dashboard")
        response = self.client.post(self.url, self.form_data)
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        response = self.client.post(response_url)
        self.assertTemplateUsed(response, "pages/dashboard.html")
        messages_list = list(response.context["messages"])
        self.assertEqual(len(messages_list), 2)
        self.assertTrue('Targets completed: ' in str(messages_list[0]))
        self.assertTrue('Targets nearly exceeded: ' in str(messages_list[1]))

    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)
