""" Unseeder CLass to clear all seeded objects from Database"""
from django.core.management.base import BaseCommand, CommandError
from django_q.models import Schedule
from financial_companion.models import (
    User,
    Account, PotAccount, BankAccount,
    CategoryTarget, UserTarget, AccountTarget, AbstractTarget,
    AbstractTransaction, Transaction, RecurringTransaction,
    Category,
    QuizQuestion,
    QuizSet,
    UserGroup,
    AbstractTarget,
    QuizScore,
    UserGroup
)
from django.db.models import QuerySet
from django_q.models import Schedule
from typing import Union
from django.db import models


class Command(BaseCommand):
    """Database Unseeder"""

    def handle(self, *args, **options) -> None:
        """Unseed Database"""
        users: User = User.objects.filter(email__endswith='@gfc.org')
        accounts: QuerySet[Account] = []
        targets: QuerySet[AbstractTarget] = []
        categories: QuerySet[Category] = []
        transactions: QuerySet[Transaction] = []
        groups: QuerySet[UserGroup] = []
        recurring_transactions: QuerySet[RecurringTransaction] = []
        quiz_scores: QuerySet[QuizScore] = []
        for user in users:
            accounts.extend(Account.objects.filter(user=user))
            targets.extend(UserTarget.objects.filter(user=user))
            categories.extend(Category.objects.filter(user=user))
            groups.extend(UserGroup.objects.filter(owner_email=user.email))
            quiz_scores.extend(QuizScore.objects.filter(user=user))

        for account in accounts:
            transactions.extend(
                Transaction.objects.filter(
                    receiver_account=account))
            transactions.extend(
                Transaction.objects.filter(
                    sender_account=account))
            targets.extend(AccountTarget.objects.filter(account_id=account))
            recurring_transactions.extend(
                RecurringTransaction.objects.filter(
                    receiver_account=account))
            recurring_transactions.extend(
                RecurringTransaction.objects.filter(
                    sender_account=account)
            )

        for category in categories:
            CategoryTarget.objects.filter(category_id=category).delete()
            category.delete()

        for transaction in transactions:
            transaction.delete()

        for account in accounts:
            account.delete()

        for quiz_score in quiz_scores:
            quiz_score.delete()
        QuizSet.objects.filter(seeded=True).delete()
        QuizQuestion.objects.filter(seeded=True).delete()

        for group in groups:
            group.delete()

        users.delete()

        Schedule.objects.all().delete()

        print("UNSEEDING COMPLETE")
