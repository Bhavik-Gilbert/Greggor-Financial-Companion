from django.core.management.base import BaseCommand, CommandError
from financial_companion.models import (
    User,
    Account, PotAccount, BankAccount,
    CategoryTarget, UserTarget, AccountTarget,
    AbstractTransaction, Transaction, #RecurringTransactions,
    Category
)

""" Unseeder CLass to clear all objects from Database"""
class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.filter(email__endswith='@gfc.org')
        potAndBankAccounts = []
        targets = []
        categories = []
        transactions = []
        for user in users:
            potAndBankAccounts.extend(PotAccount.objects.filter(user_id = user))
            targets.extend(UserTarget.objects.filter(user_id = user))
            categories.extend(Category.objects.filter(user = user))
        
        for account in potAndBankAccounts:
            transactions.extend(Transaction.objects.filter(receiver_account = account))
            transactions.extend(Transaction.objects.filter(sender_account = account))
            targets.extend(AccountTarget.objects.filter(account_id = account))
                
        for category in categories:
            CategoryTarget.objects.filter(category_id = category).delete()
            category.delete()

        for transaction in transactions:
            transaction.delete()
        
        for account in potAndBankAccounts:
            account.delete()
        
        users.delete()
