from django.core.management.base import BaseCommand, CommandError
from financial_companion.models import (
    User,
    Account, PotAccount, BankAccount,
    CategoryTarget, UserTarget, AccountTarget,
    Transaction, #RecurringTransactions,
    Category
)

""" Unseeder CLass to clear all objects from Database"""
class Command(BaseCommand):
    def handle(self, *args, **options):
        User.objects.all().delete()
        Account.objects.all().delete()
        CategoryTarget.objects.all().delete()
        UserTarget.objects.all().delete()
        AccountTarget.objects.all().delete()
        Transaction.objects.all().delete()
        Category.objects.all().delete()