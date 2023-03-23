"""Tests of the seed and unseed command"""
from django.core.management import call_command
from django.db.models import QuerySet
from .test_management_base import ManagementTestCase

from financial_companion.models import (
    User, UserGroup,
    Account, PotAccount, BankAccount,
    CategoryTarget, UserTarget, AccountTarget,
    Transaction, RecurringTransaction,
    Category,
    QuizQuestion, QuizScore, QuizSet
)
from django_q.models import Schedule
from django.db.models import Q


class ManagementSeedTestCase(ManagementTestCase):
    """Test class for seed and unseed commands"""

    def _assert_successfully_seed(self) -> None:
        """Assert that we can seed the database"""
        call_command("seed")

        user_count: int = User.objects.count()
        # check we created atleast 4 users
        self.assertTrue(user_count >= 4)
        # check all schedulers created
        self.assertTrue(Schedule.objects.count() >= 3)
        # check all questions read from file
        self.assertEqual(QuizQuestion.objects.count(), 20)

        # check database seeded correctly
        self.assertTrue(Category.objects.count() >= 3 * (user_count - 2))
        self.assertTrue(Account.objects.count() >= 3 * (user_count - 2))
        self.assertTrue(PotAccount.objects.count() >= 2 * (user_count - 2))
        self.assertTrue(BankAccount.objects.count() >= 1 * (user_count - 2))
        self.assertTrue(Transaction.objects.count() > 0)
        self.assertTrue(RecurringTransaction.objects.count() > 0)
        self.assertTrue(UserGroup.objects.count() > 0)
        self.assertTrue(CategoryTarget.objects.count() > 0)
        self.assertTrue(UserTarget.objects.count() > 0)
        self.assertTrue(AccountTarget.objects.count() > 0)
        self.assertTrue(QuizSet.objects.count() > 0)
        self.assertTrue(QuizScore.objects.count() >= QuizSet.objects.count())

    def _assert_successfully_unseed(self, seeded_users: QuerySet[User]):
        """Assert that we can unseed the database"""
        call_command("unseed")

        # check everything that was seeded was deleted
        seeded_user_accounts: QuerySet[Account] = Account.objects.filter(
            user__in=seeded_users)
        seeded_user_categories: QuerySet[Category] = Category.objects.filter(
            user__in=seeded_users)
        seeded_user_emails: list[str] = []
        self.assertEqual(
            User.objects.filter(
                email__endswith='@gfc.org').count(), 0)
        self.assertEqual(Schedule.objects.count(), 0)
        self.assertEqual(QuizSet.objects.filter(seeded=True).count(), 0)
        self.assertEqual(QuizQuestion.objects.filter(seeded=True).count(), 0)
        self.assertEqual(
            QuizScore.objects.filter(
                user__in=seeded_users).count(), 0)
        self.assertEqual(
            BankAccount.objects.filter(
                user__in=seeded_users).count(), 0)
        self.assertEqual(
            PotAccount.objects.filter(
                user__in=seeded_users).count(), 0)
        self.assertEqual(seeded_user_accounts.count(), 0)
        self.assertEqual(seeded_user_categories.count(), 0)
        self.assertEqual(Transaction.objects.filter(
            Q(sender_account__in=seeded_user_accounts) |
            Q(receiver_account__in=seeded_user_accounts)
        ).count(), 0)
        self.assertEqual(RecurringTransaction.objects.filter(
            Q(sender_account__in=seeded_user_accounts) |
            Q(receiver_account__in=seeded_user_accounts)
        ).count(), 0)
        self.assertEqual(
            UserTarget.objects.filter(
                user__in=seeded_users).count(), 0)
        self.assertEqual(AccountTarget.objects.filter(
            account__in=seeded_user_accounts).count(), 0)
        self.assertEqual(CategoryTarget.objects.filter(
            category__in=seeded_user_categories).count(), 0)
        self.assertEqual(
            UserGroup.objects.filter(
                owner_email__in=seeded_user_emails).count(), 0)

    def test_successfully_seed_and_unseed(self) -> None:
        """Tests that we can seed and unseed the database"""
        self._assert_successfully_seed()
        seeded_users: QuerySet[User] = User.objects.filter(
           email__endswith='@gfc.org')
        self._assert_successfully_unseed(seeded_users)
