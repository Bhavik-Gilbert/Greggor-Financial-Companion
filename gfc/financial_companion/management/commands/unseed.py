from django.core.management.base import BaseCommand, CommandError
from financial_companion.models import (
    User,
    Account, PotAccount, BankAccount,
    CategoryTarget, UserTarget, AccountTarget,
    AbstractTransaction, Transaction, RecurringTransaction,
    Category,
    QuizQuestion,
    QuizSet,
    UserGroup
)

""" Unseeder CLass to clear all objects from Database"""


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.filter(email__endswith='@gfc.org')
        Accounts = []
        targets = []
        categories = []
        transactions = []
        groups = []
        recurringTransactions = []
        for user in users:
            Accounts.extend(Account.objects.filter(user=user))
            targets.extend(UserTarget.objects.filter(user=user))
            categories.extend(Category.objects.filter(user=user))
            groups.extend(UserGroup.objects.filter(owner_email=user.email))

        for account in Accounts:
            transactions.extend(
                Transaction.objects.filter(
                    receiver_account=account))
            transactions.extend(
                Transaction.objects.filter(
                    sender_account=account))
            targets.extend(AccountTarget.objects.filter(account_id=account))
            recurringTransactions.extend(
                RecurringTransaction.objects.filter(
                    receiver_account=account))
            recurringTransactions.extend(
                RecurringTransaction.objects.filter(
                    sender_account = account)
                )

        for category in categories:
            CategoryTarget.objects.filter(category_id=category).delete()
            category.delete()

        for transaction in transactions:
            transaction.delete()

        for account in Accounts:
            account.delete()

        QuizSet.objects.filter(seeded=True).delete()
        QuizQuestion.objects.filter(seeded=True).delete()

        for group in groups:
            group.delete()

        users.delete()
