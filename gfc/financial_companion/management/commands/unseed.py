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
        User.objects.filter(email__endswith='@gfc.org').delete()