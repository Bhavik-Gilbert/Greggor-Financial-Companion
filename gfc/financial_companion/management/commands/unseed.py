""" Unseeder Class to clear all seeded objects from Database"""
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
        print(f"UNSEEDING IN PROGRESS",end='\r')
        
        users: QuerySet[User] = User.objects.filter(email__endswith='@gfc.org')
        users.delete()

        print(f"UNSEEDING COMPLETE",end='\r')

    def hi(self):
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
            print(f'DELETING Category {category}',end='\r')
            CategoryTarget.objects.filter(category_id=category).delete()
            category.delete()

        for transaction in transactions:
            print(f'DELETING Transaction {transaction.id}',end='\r')
            transaction.delete()

        for account in accounts:
            print(f"DELETING Account {account.id}",end='\r')
            account.delete()

        for quiz_score in quiz_scores:
            print(f"DELETING Quiz Score {quiz_score.id}",end='\r')
            quiz_score.delete()
        QuizSet.objects.filter(seeded=True).delete()
        QuizQuestion.objects.filter(seeded=True).delete()

        for group in groups:
            print(f"DELETING Group {group.id}",end='\r')
            group.delete()

        users.delete()

        Schedule.objects.all().delete()