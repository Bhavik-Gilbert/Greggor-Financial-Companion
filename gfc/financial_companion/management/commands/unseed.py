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
        quiz_scores: QuerySet[QuizScore] = QuizScore.objects.filter(user__in=user)

        users.delete()
        quiz_scores.delete()
        Schedule.objects.all().delete()

        QuizSet.objects.filter(seeded=True).delete()
        QuizQuestion.objects.filter(seeded=True).delete()

        print(f"UNSEEDING COMPLETE",end='\r')
        