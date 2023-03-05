from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
import os
from financial_companion.helpers import random_filename
import financial_companion.models as fcmodels


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

        all_targets = []

        all_user_targets = fcmodels.UserTarget.objects.filter(user=user)

        all_accounts = fcmodels.PotAccount.objects.filter(user=user.id)
        all_account_targets = []
        for account in all_accounts:
            all_account_targets = [
                *all_account_targets,
                *fcmodels.AccountTarget.objects.filter(account=account)
            ]

        all_categories = fcmodels.Category.objects.filter(user=user)
        all_category_targets = []
        for category in all_categories:
            all_category_targets = [
                *all_category_targets,
                *fcmodels.CategoryTarget.objects.filter(category=category)
            ]

        all_targets = [
            *all_targets,
            *all_user_targets,
            *all_account_targets,
            *all_category_targets]

        return all_targets

    def get_number_of_completed_targets(user):
        total = 0
        targets = self.get_all_targets()
        for target in targets:
            if target.is_complete:
                total += 1
        return total
