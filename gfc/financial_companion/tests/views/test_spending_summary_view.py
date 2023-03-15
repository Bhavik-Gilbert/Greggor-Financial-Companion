from .test_view_base import ViewTestCase
from financial_companion.forms import TimespanOptionsForm
from financial_companion.models import User, Transaction
from financial_companion.helpers.enums import Timespan
from financial_companion.helpers import functions
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from freezegun import freeze_time
from datetime import datetime

class SpendingSummaryViewTestCase(ViewTestCase):
    """Test Case for user spending summary page."""
    def setUp(self):
        self.url = reverse('spending_summary')
        self.test_model: Transaction = Transaction.objects.get(id=4)
        self.user = User.objects.get(id=1)


    def test_spending_summary_url(self):
        self.assertEqual(self.url, '/spending_summary/')

    @freeze_time("2023-01-07 22:00:00")
    def test_valid_within_time_period(self):
            self.assertEqual(
                len(Transaction.get_transactions_from_time_period(Timespan.WEEK, self.user)), 8)

    @freeze_time("2023-01-01 22:00:00")
    def test_get_spending_summary_page(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/spending_summary.html")
        form: TimespanOptionsForm = response.context["form"]
        self.assertTrue(isinstance(form, TimespanOptionsForm))
        time: Timespan = Timespan.WEEK
        self.assertTrue(isinstance(time, Timespan))
        total_spent = Transaction.calculate_total(
            Transaction.get_transactions_from_time_period(
                time, self.user, "sent"))
        total_received = Transaction.calculate_total(
            Transaction.get_transactions_from_time_period(
                time, self.user, "received"))
        categories = Transaction.get_category_splits(
            Transaction.get_transactions_from_time_period(
                time, self.user, "sent"), self.user)
        percentages = functions.calculate_percentages(categories, total_spent)
        percentages_list = list(percentages.values())
        labels = list(percentages.keys())

        keyset: list[str] = response.context["keyset"]
        self.assertEqual(keyset, labels)
        dataset: list[float] = response.context["dataset"]
        self.assertEqual(dataset, percentages_list)
        money_in: float = response.context["money_in"]
        self.assertEqual(money_in, total_received)
        money_out: float = response.context["money_out"]
        self.assertEqual(money_out, total_spent)
       

    @freeze_time("1998-01-07 22:00:00")
    def test_get_spending_summary_page_no_transactions(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/spending_summary.html")
        form: TimespanOptionsForm = response.context["form"]
        self.assertTrue(isinstance(form, TimespanOptionsForm))
        time: Timespan = Timespan.DAY
        self.assertTrue(isinstance(time, Timespan))
        transactions = Transaction.get_transactions_from_time_period(
                time, self.user, "sent")
        self.assertEqual(len(transactions), 0)
        total_spent = Transaction.calculate_total(transactions)
        self.assertEqual(total_spent, 0)
        total_received = Transaction.calculate_total(
            Transaction.get_transactions_from_time_period(
                time, self.user, "received"))
        self.assertEqual(total_received, 0)
        categories = Transaction.get_category_splits(transactions, self.user)
        self.assertEqual(len(categories), 0)    
        percentages = functions.calculate_percentages(categories, total_spent)
        self.assertEqual(len(percentages), 0)
        percentages_list = list(percentages.values())
        self.assertEqual(len(percentages_list),0)
        labels = list(percentages.keys())
        self.assertEqual(len(labels), 0)
        if percentages_list == []:
            percentages_list = None

        keyset: list[str] = response.context["keyset"]
        self.assertEqual(keyset, labels)
        dataset: list[float] = response.context["dataset"]
        self.assertEqual(dataset, percentages_list)
        money_in: float = response.context["money_in"]
        self.assertEqual(money_in, total_received)
        money_out: float = response.context["money_out"]
        self.assertEqual(money_out, total_spent)
    
    
    @freeze_time("2023-01-01 22:00:00")
    def test_change_timespan_spending_summary_page(self):
        self._login(self.user)
        time: Timespan = Timespan.WEEK
        self.assertTrue(isinstance(time, Timespan))
        response = self.client.post(self.url, {"time_choice": "day"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/spending_summary.html")
        form: TimespanOptionsForm = response.context["form"]
        self.assertTrue(isinstance(form, TimespanOptionsForm))
        total_spent = Transaction.calculate_total(
            Transaction.get_transactions_from_time_period(
                time, self.user, "sent"))
        total_received = Transaction.calculate_total(
            Transaction.get_transactions_from_time_period(
                time, self.user, "received"))
        categories = Transaction.get_category_splits(
            Transaction.get_transactions_from_time_period(
                time, self.user, "sent"), self.user)
        percentages = functions.calculate_percentages(categories, total_spent)
        percentages_list = list(percentages.values())
        labels = list(percentages.keys())

        keyset: list[str] = response.context["keyset"]
        self.assertEqual(keyset, labels)
        dataset: list[float] = response.context["dataset"]
        self.assertEqual(dataset, percentages_list)
        money_in: float = response.context["money_in"]
        self.assertEqual(money_in, total_received)
        money_out: float = response.context["money_out"]
        self.assertEqual(money_out, total_spent)
       

