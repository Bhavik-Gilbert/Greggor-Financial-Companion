from .test_template_tag_base import TemplateTagTestCase
from financial_companion.models import CategoryTarget, AccountTarget, UserTarget
from financial_companion.helpers import timespan_map, TransactionType, convert_currency
from financial_companion.templatetags import get_completeness
from freezegun import freeze_time
import datetime


class GetCompletenessTemplateTagTestCase(TemplateTagTestCase):
    """Test for the get_completeness template tag"""

    def _get_all_transactions(self, target):
        transactions = []
        if isinstance(target, CategoryTarget):
            transactions = target.category.get_category_transactions()
        elif isinstance(target, AccountTarget):
            account = target.account
            if target.target_type == TransactionType.INCOME:
                transactions = account.get_account_transactions("sent")
            else:
                transactions = account.get_account_transactions("received")
        elif isinstance(target, UserTarget):
            transactions = target.user.get_user_transactions()
        return transactions

    def _get_start_of_time_period(self, target):
        timespan_int = timespan_map[target.timespan]
        start_of_timespan_period = datetime.date.today(
        ) - datetime.timedelta(days=timespan_int)
        return start_of_timespan_period

    def _filter_transactions(self, start, transactions):
        filtered_transactions = []
        for transaction in transactions:
            if transaction.time_of_transaction.date(
            ) >= start and transaction.time_of_transaction.date() <= datetime.date.today():
                filtered_transactions = [*filtered_transactions, transaction]
        return filtered_transactions

    def _calculate_completeness(self, target, transactions):
        total = 0.0
        for transaction in transactions:
            total += float(convert_currency(transaction.amount, transaction.currency, target.currency))

        amount = target.amount
        if amount == 0:
            return round(0, 2)
        else:
            completeness = (total / float(amount)) * 100
            return round(completeness, 2)

    def setUp(self):
        self.account_target: AccountTarget = AccountTarget.objects.get(id=1)
        self.account_target_2: AccountTarget = AccountTarget.objects.get(id=5)
        self.category_target: CategoryTarget = CategoryTarget.objects.get(id=1)
        self.user_target: UserTarget = UserTarget.objects.get(id=1)

    def test_get_transaction_for_category_target(self):
        transactions = self.category_target.category.get_category_transactions()
        self.assertEqual(
            transactions,
            self._get_all_transactions(
                self.category_target))

    def test_get_transaction_for_account_target(self):
        account = self.account_target.account
        if self.account_target.target_type == TransactionType.INCOME:
            transactions = account.get_account_transactions("sent")
        else:
            transactions = account.get_account_transactions("received")
        self.assertEqual(
            transactions,
            self._get_all_transactions(
                self.account_target))

    def test_get_transaction_for_user_target(self):
        transactions = self.user_target.user.get_user_transactions()
        self.assertEqual(
            transactions,
            self._get_all_transactions(
                self.user_target))

    # test the filter transaction on each different time span
    # freeze time is year month day
    @freeze_time("2023-01-01 13:00:00")
    def test_filter_transactions_with_timespan_day_and_time_within_a_day(self):
        target: CategoryTarget = self.category_target
        non_filtered = target.category.get_category_transactions()
        start = self._get_start_of_time_period(target)
        filtered = self._filter_transactions(start, non_filtered)
        self.assertEqual(non_filtered, filtered)

    @freeze_time("2023-01-03 14:00:00")
    def test_filter_transactions_with_timespan_day_and_time_outside_a_day(
            self):
        target: CategoryTarget = self.category_target
        non_filtered = target.category.get_category_transactions()
        start = self._get_start_of_time_period(target)
        filtered = self._filter_transactions(start, non_filtered)
        self.assertNotEqual(non_filtered, filtered)

    @freeze_time("2023-01-4 18:00:00")
    def test_filter_transactions_with_timespan_week_and_time_within_a_week(
            self):
        target: CategoryTarget = CategoryTarget.objects.get(id=3)
        non_filtered = target.category.get_category_transactions()
        start = self._get_start_of_time_period(target)
        filtered = self._filter_transactions(start, non_filtered)
        self.assertEqual(non_filtered, filtered)

    @freeze_time("2023-01-21 18:00:00")
    def test_filter_transactions_with_timespan_week_and_time_outside_a_week(
            self):
        target: CategoryTarget = CategoryTarget.objects.get(id=3)
        non_filtered = target.category.get_category_transactions()
        start = self._get_start_of_time_period(target)
        filtered = self._filter_transactions(start, non_filtered)
        self.assertNotEqual(non_filtered, filtered)

    @freeze_time("2023-01-25 18:00:00")
    def test_filter_transactions_with_timespan_month_and_time_within_a_month(
            self):
        target: CategoryTarget = CategoryTarget.objects.get(id=4)
        non_filtered = target.category.get_category_transactions()
        start = self._get_start_of_time_period(target)
        filtered = self._filter_transactions(start, non_filtered)
        self.assertEqual(non_filtered, filtered)

    @freeze_time("2023-03-01 18:00:00")
    def test_filter_transactions_with_timespan_month_and_time_outside_a_month(
            self):
        target: CategoryTarget = CategoryTarget.objects.get(id=4)
        non_filtered = target.category.get_category_transactions()
        start = self._get_start_of_time_period(target)
        filtered = self._filter_transactions(start, non_filtered)
        self.assertNotEqual(non_filtered, filtered)

    @freeze_time("2023-11-11 18:00:00")
    def test_filter_transactions_with_timespan_year_and_time_within_a_year(
            self):
        target: CategoryTarget = CategoryTarget.objects.get(id=5)
        non_filtered = target.category.get_category_transactions()
        start = self._get_start_of_time_period(target)
        filtered = self._filter_transactions(start, non_filtered)
        self.assertEqual(non_filtered, filtered)

    @freeze_time("2025-01-01 18:00:00")
    def test_filter_transactions_with_timespan_year_and_time_outside_a_year(
            self):
        target: CategoryTarget = CategoryTarget.objects.get(id=5)
        non_filtered = target.category.get_category_transactions()
        start = self._get_start_of_time_period(target)
        filtered = self._filter_transactions(start, non_filtered)
        self.assertNotEqual(non_filtered, filtered)

    # test the completeness on each target:
    @freeze_time("2023-01-01 12:00:00")
    def test_get_completeness_for_category_target(self):
        target = self.category_target
        transactions = self._get_all_transactions(target)
        start = self._get_start_of_time_period(target)
        filtered = self._filter_transactions(start, transactions)
        completeness = self._calculate_completeness(target, filtered)
        completeness_from_tag = get_completeness(target)
        self.assertEqual(completeness, completeness_from_tag)

    @freeze_time("2023-01-01 12:00:00")
    def test_get_completeness_for_account_target(self):
        target = self.account_target
        completeness_from_tag = get_completeness(target)
        self.assertEqual(499.99, completeness_from_tag)

    @freeze_time("2023-01-01 12:00:00")
    def test_get_completeness_for_account_target_with_zero_amount(self):
        target = self.account_target_2
        transactions = self._get_all_transactions(target)
        start = self._get_start_of_time_period(target)
        filtered = self._filter_transactions(start, transactions)
        completeness = self._calculate_completeness(target, filtered)
        completeness_from_tag = get_completeness(target)
        self.assertEqual(completeness, 0)
        self.assertEqual(completeness_from_tag, 0)

    @freeze_time("2023-01-01 12:00:00")
    def test_get_completeness_for_user_target(self):
        target = self.user_target
        transactions = self._get_all_transactions(target)
        start = self._get_start_of_time_period(target)
        filtered = self._filter_transactions(start, transactions)
        completeness = self._calculate_completeness(target, filtered)
        completeness_from_tag = get_completeness(target)
        self.assertEqual(completeness, completeness_from_tag)
