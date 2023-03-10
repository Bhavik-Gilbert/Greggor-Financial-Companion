from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
import os
from financial_companion.helpers import random_filename
import financial_companion.models as fcmodels
from ..helpers import TransactionType


def change_filename(instance, filename):
    return os.path.join('user_profile', random_filename(filename))


class User(AbstractUser):
    """User model used for authentication"""

    username: models.CharField = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{1,}$',
            message='Username must consist of @ followed by at least one letter or number'
        )]
    )
    first_name: models.CharField = models.CharField(max_length=50, blank=False)
    last_name: models.CharField = models.CharField(max_length=50, blank=False)
    email: models.EmailField = models.EmailField(unique=True, blank=False)
    bio: models.CharField = models.CharField(max_length=520, blank=True)
    profile_picture: models.ImageField = models.ImageField(
        upload_to=change_filename,
        height_field=None,
        width_field=None,
        max_length=100,
        blank=True)

    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'

    def get_user_transactions(self, filter_type: str = "all") -> list:
        """Return filtered list of the users transactions"""
        user_accounts: list[fcmodels.PotAccount] = fcmodels.PotAccount.objects.filter(
            user=self)
        transactions: list[fcmodels.Transaction] = []

        for account in user_accounts:
            transactions = [
                *transactions,
                *account.get_account_transactions(filter_type)]

        return sorted(
            transactions, key=lambda transaction: transaction.time_of_transaction, reverse=True)

    def get_user_recurring_transactions(self) -> list:
        user_accounts: list[fcmodels.PotAccount] = fcmodels.PotAccount.objects.filter(
            user=self)
        transactions: list[fcmodels.RecurringTransaction]= []

        for account in user_accounts:
            transactions= [
                *transactions,
                *account.get_account_recurring_transactions()
            ]
        return transactions

    def get_user_highest_quiz_score(self):
        """Return users highest quiz score"""
        user_scores: list[fcmodels.QuizScore] = fcmodels.QuizScore.objects.filter(
            user=self
        )
        return max(user_scores, key=lambda quiz_score: quiz_score.get_score())

    def get_all_targets(self):
        user = self
        user_targets = fcmodels.UserTarget.objects.filter(user=user)
        user_account_targets = self.get_all_account_targets()
        user_category_targets = self.get_all_category_targets()

        return [*user_targets, *user_account_targets, *user_category_targets]

    def get_all_account_targets(self, accounts=None):
        user = self
        if not accounts:
            accounts = fcmodels.PotAccount.objects.filter(user=user)
        user_account_targets = fcmodels.AccountTarget.objects.filter(
            account__in=accounts)

        return list(user_account_targets)

    def get_all_category_targets(self, categories=None):
        user = self
        if not categories:
            categories = fcmodels.Category.objects.filter(user=user)
        user_category_targets = fcmodels.CategoryTarget.objects.filter(
            category__in=categories)

        return list(user_category_targets)

    def get_completed_targets(self, targets):
        filtered_targets = []
        for target in targets:
            if target.is_complete():
                filtered_targets.append(target)
        return filtered_targets

    def get_nearly_completed_targets(self, targets):
        filtered_targets = []
        for target in targets:
            if target.is_nearly_complete():
                filtered_targets.append(target)
        return filtered_targets

    def get_number_of_nearly_completed_targets(self):
        return self.get_number_of_nearly_completed_spending_targets(
        ) + self.get_number_of_nearly_completed_saving_targets()

    def get_number_of_nearly_completed_spending_targets(self):
        total = 0
        targets = self.get_all_targets()
        for target in targets:
            if target.is_nearly_complete() and target.target_type == TransactionType.INCOME:
                total += 1
        return total

    def get_number_of_nearly_completed_saving_targets(self):
        total = 0
        targets = self.get_all_targets()
        for target in targets:
            if target.is_nearly_complete() and target.target_type == TransactionType.EXPENSE:
                total += 1
        return total

    def get_number_of_completed_targets(self):
        return self.get_number_of_completed_spending_targets(
        ) + self.get_number_of_completed_saving_targets()

    def get_number_of_completed_spending_targets(self):
        total = 0
        targets = self.get_all_targets()
        for target in targets:
            if target.is_complete() and target.target_type == TransactionType.INCOME:
                total += 1
        return total

    def get_number_of_completed_saving_targets(self):
        total = 0
        targets = self.get_all_targets()
        for target in targets:
            if target.is_complete() and target.target_type == TransactionType.EXPENSE:
                total += 1
        return total

    def get_leaderboard_score(self):
        score = 0
        score += -(0.5 * self.get_number_of_completed_spending_targets()) + self.get_number_of_completed_saving_targets() + \
            self.get_number_of_nearly_completed_saving_targets(
        ) + -(0.5 * self.get_number_of_nearly_completed_spending_targets())
        return score
