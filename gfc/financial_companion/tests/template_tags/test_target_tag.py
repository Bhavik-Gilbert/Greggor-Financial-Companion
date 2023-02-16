from .test_template_tag_base import TemplateTagTestCase
from financial_companion.models import Transaction, CategoryTarget, AccountTarget, UserTarget
from financial_companion.helpers import timespan_map
from financial_companion.templatetags import get_completeness
import os
from freezegun import freeze_time
import datetime


class GetCompletenessTemplateTagTestCase(TemplateTagTestCase):
    """Test for the get_completeness logo template tag"""

    def _get_all_transactions(self, target):
        transactions = []
        if isinstance(target, CategoryTarget):
            transactions = target.category.get_category_transactions()
        elif isinstance(target, AccountTarget):
            transactions = target.account.get_account_transactions()
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
            if transaction.time_of_transaction.date() >= start:
                filtered_transactions = [*filtered_transactions, transaction]
        return filtered_transactions

    def _calculate_completeness(self, target, transactions):
        total = 0.0
        for transaction in transactions:
            total += float(transaction.amount)
        completeness = (total / float(target.amount)) * 100
        return round(completeness, 2)

    def setUp(self):
        self.account_target: AccountTarget = AccountTarget.objects.get(id = 1)
        self.category_target: CategoryTarget = CategoryTarget.objects.get(id = 1)
        self.user_target: UserTarget = UserTarget.objects.get(id = 1)

    # TODO: need to write tests

    # "2023-01-01T12:00:00+00:00" - each transaction has this for its time

    # @freeze_time("2023-01-01 12:00:00")

    def test_get_transaction_for_category_target(self):
        transactions = self.category_target.category.get_category_transactions()
        self.assertEqual(transactions, self._get_all_transactions(self.category_target))

    def test_get_transaction_for_account_target(self):
        transactions = self.account_target.account.get_account_transactions()
        self.assertEqual(transactions, self._get_all_transactions(self.account_target))

    def test_get_transaction_for_user_target(self):
        transactions = self.user_target.user.get_user_transactions()
        self.assertEqual(transactions, self._get_all_transactions(self.user_target))

    # test the filter trnasaction on each different time span
    @freeze_time("2023-01-01 12:00:00")
    def test_filter_transactions_with_timespan_day_and_time_within_a_day(self):
        target: CategoryTarget = CategoryTarget.objects.get(id = 5)
        non_filtered = target.category.get_category_transactions()

    @freeze_time("2023-01-01 18:00:00")
    def test_filter_transactions_with_timespan_day_and_time_outside_a_day(self):
        target: CategoryTarget = CategoryTarget.objects.get(id = 5)
        non_filtered = target.category.get_category_transactions()

    def test_filter_transactions_with_timespan_week(self):
        target: CategoryTarget = CategoryTarget.objects.get(id = 2)
        non_filtered = target.category.get_category_transactions()

    def test_filter_transactions_with_timespan_month(self):
        target: CategoryTarget = CategoryTarget.objects.get(id = 3)
        non_filtered = target.category.get_category_transactions()

    def test_filter_transactions_with_timespan_year(self):
        target: CategoryTarget = CategoryTarget.objects.get(id = 4)
        non_filtered = target.category.get_category_transactions()

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
        transactions = self._get_all_transactions(target)
        start = self._get_start_of_time_period(target)
        filtered = self._filter_transactions(start, transactions)
        completeness = self._calculate_completeness(target, filtered)
        completeness_from_tag = get_completeness(target)
        self.assertEqual(completeness, completeness_from_tag)

    @freeze_time("2023-01-01 12:00:00")
    def test_get_completeness_for_user_target(self):
        target = self.user_target
        transactions = self._get_all_transactions(target)
        start = self._get_start_of_time_period(target)
        filtered = self._filter_transactions(start, transactions)
        completeness = self._calculate_completeness(target, filtered)
        completeness_from_tag = get_completeness(target)
        self.assertEqual(completeness, completeness_from_tag)
