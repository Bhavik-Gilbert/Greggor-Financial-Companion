from .test_view_base import ViewTestCase
from financial_companion.forms import TimespanCurrencyOptionsForm
from financial_companion.models import User, Transaction
from financial_companion.helpers.enums import (
    Timespan, FilterTransactionType, CurrencyType
)
from financial_companion.helpers import functions
from django.urls import reverse
from django.http import HttpResponse
from freezegun import freeze_time
from decimal import Decimal


class SpendingSummaryViewTestCase(ViewTestCase):
    """Test Case for user spending summary page."""

    def setUp(self):
        self.url: str = reverse('spending_summary')
        self.test_model: Transaction = Transaction.objects.get(id=4)
        self.user: User = User.objects.get(id=1)

    def test_spending_summary_url(self):
        self.assertEqual(self.url, '/spending_summary/')
        url_with_params: str = reverse('spending_summary', kwargs={
            "time": Timespan.DAY, "currency": CurrencyType.GBP
        })
        self.assertEqual(url_with_params, '/spending_summary/day/GBP/')

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
        form: TimespanCurrencyOptionsForm = response.context["form"]
        self.assertTrue(isinstance(form, TimespanCurrencyOptionsForm))
        time: Timespan = response.context["time"].lower()
        self.assertTrue(time in Timespan)
        currency: CurrencyType = response.context["currency"]
        self.assertTrue(currency in CurrencyType)
        transactions_spent: list[Transaction] = Transaction.get_transactions_from_time_period(
            time, self.user, FilterTransactionType.SENT
        )
        total_spent: float = Transaction.calculate_total_amount_from_transactions(
            transactions_spent
        )
        total_received: float = Transaction.calculate_total_amount_from_transactions(
            Transaction.get_transactions_from_time_period(
                time, self.user, FilterTransactionType.RECEIVED
            )
        )
        category_amounts: dict[str, Decimal] = Transaction.get_category_splits(
            transactions_spent, self.user)
        percentages: dict[str, float] = functions.calculate_split_percentages(
            category_amounts)
        percentages_list: list[float] = list(percentages.values())
        labels: list[str] = list(percentages.keys())

        keyset: list[str] = response.context["keyset"]
        self.assertEqual(keyset, labels)
        dataset: list[float] = response.context["dataset"]
        self.assertEqual(dataset, percentages_list)
        money_in: Decimal = response.context["money_in"]
        self.assertEqual(money_in, total_received)
        money_out: Decimal = response.context["money_out"]
        self.assertEqual(money_out, total_spent)

    @freeze_time("1998-01-07 22:00:00")
    def test_get_spending_summary_page_no_transactions(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/spending_summary.html")
        form: TimespanCurrencyOptionsForm = response.context["form"]
        self.assertTrue(isinstance(form, TimespanCurrencyOptionsForm))
        time: Timespan = Timespan.DAY
        self.assertTrue(isinstance(time, Timespan))
        transactions_sent: list[Transaction] = Transaction.get_transactions_from_time_period(
            time, self.user, FilterTransactionType.SENT)
        transactions_received: list[Transaction] = Transaction.get_transactions_from_time_period(
            time, self.user, FilterTransactionType.RECEIVED)
        self.assertEqual(len(transactions_sent), 0)
        total_spent: float = Transaction.calculate_total_amount_from_transactions(
            transactions_sent
        )
        self.assertEqual(total_spent, 0)
        total_received: float = Transaction.calculate_total_amount_from_transactions(
            transactions_received
        )
        self.assertEqual(total_received, 0)
        category_amounts = Transaction.get_category_splits(
            transactions_sent, self.user)
        self.assertEqual(len(category_amounts), 0)
        percentages = functions.calculate_split_percentages(category_amounts)
        self.assertEqual(len(percentages), 0)
        percentages_list = list(percentages.values())
        self.assertEqual(len(percentages_list), 0)
        labels = list(percentages.keys())
        self.assertEqual(len(labels), 0)
        if percentages_list == []:
            percentages_list = None

        keyset: list[str] = response.context["keyset"]
        self.assertEqual(keyset, labels)
        dataset: list[float] = response.context["dataset"]
        self.assertEqual(dataset, percentages_list)
        money_in: Decimal = response.context["money_in"]
        self.assertEqual(money_in, total_received)
        money_out: Decimal = response.context["money_out"]
        self.assertEqual(money_out, total_spent)

    @freeze_time("2023-01-01 22:00:00")
    def test_valid_form_inputs_spending_summary_page(self):
        self._login(self.user)
        time: Timespan = Timespan.WEEK
        currency: CurrencyType = CurrencyType.USD
        self.assertTrue(isinstance(time, Timespan))
        self.assertTrue(isinstance(currency, CurrencyType))
        response = self.client.post(
            self.url, {"time_choice": time, "currency_choice": currency},
            follow=True
        )
        response_url: str = reverse("spending_summary", kwargs={
            "time": time, "currency": currency
        })
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, "pages/spending_summary.html")
    
    @freeze_time("2023-01-01 22:00:00")
    def test_get_invalid_timespan_spending_summary_page(self):
        self._login(self.user)
        time: str = "invalid"
        currency: CurrencyType = CurrencyType.USD
        self.assertFalse(isinstance(time, Timespan))
        self.assertTrue(isinstance(currency, CurrencyType))
        url_with_params: str = reverse('spending_summary', kwargs={
            "time": time, "currency": currency
        })
        response = self.client.get(url_with_params, follow=True)
        self.assertRedirects(
            response,
            self.url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, "pages/spending_summary.html")
    
    @freeze_time("2023-01-01 22:00:00")
    def test_get_invalid_currency_spending_summary_page(self):
        self._login(self.user)
        time: Timespan = Timespan.WEEK
        currency: str = "invalid"
        self.assertTrue(isinstance(time, Timespan))
        self.assertFalse(isinstance(currency, CurrencyType))
        url_with_params: str = reverse('spending_summary', kwargs={
            "time": time, "currency": currency
        })
        response = self.client.get(url_with_params, follow=True)
        self.assertRedirects(
            response,
            self.url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, "pages/spending_summary.html")
    
    def test_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)