from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from financial_companion.models import (
    User,
    Account, PotAccount, BankAccount,
    CategoryTarget, UserTarget, AccountTarget,
    Transaction, #RecurringTransactions,
    Category
)
from django.db.utils import IntegrityError
import datetime
from random import randint, random
import random
from financial_companion.helpers import TransactionType, CurrencyType, MonetaryAccountType, Timespan

class Command(BaseCommand):
    PASSWORD = "Password123"
    USER_COUNT = 1
    MAX_ACCOUNTS_PER_USER = 10
    MAX_TRANSACTIONS_PER_ACCOUNT = 50
    MAX_NUMBER_OF_CATEGORIES = 20
    OBJECT_HAS_TARGET_PROBABILITY = 0.6

    def __init__(self):
        super().__init__()
        self.faker = Faker("en_GB")

    def handle(self, *args, **options):
        self.create_categories()
        self.create_users()
        print("SEEDING COMPLETE")

    def create_categories(self):
        randomNumOfCategories = randint(3, self.MAX_NUMBER_OF_CATEGORIES)
        self.categories = []
        for i in range(0, randomNumOfCategories):
            category = Category.objects.create(
                    name = self.faker.word(),
                    description = self.faker.text()
                )
            self.categories.append(category)
            if (float(randint(0,100))/100 < self.OBJECT_HAS_TARGET_PROBABILITY):
                CategoryTarget.objects.create(
                    transaction_type = self.choose_random_enum(TransactionType),
                    timespan = self.choose_random_enum(Timespan),
                    amount = float(randint(0,1000000))/100,
                    currency = self.choose_random_enum(CurrencyType),
                    category_id = category
                )
    
    def create_users(self):
        self.create_single_user("Michael", "Kolling", self.PASSWORD, True)
        self.create_single_user("admin", "user", self.PASSWORD, True)
        while User.objects.count() < self.USER_COUNT:
            self.create_single_user(self.faker.first_name(), self.faker.last_name(), self.PASSWORD, False)
        print("USERS SEEDED")
    
    def create_single_user(self, first_name, last_name, password, adminStatus):
        try:
            user = User.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                username = self.format_username(first_name,last_name),
                email = self.format_email(first_name,last_name),
                password = password,
                bio = self.faker.text(),
                is_staff = adminStatus,
                is_superuser = adminStatus
            )
            if (not(adminStatus)):
                if (float(randint(0,100))/100 < self.OBJECT_HAS_TARGET_PROBABILITY):
                    UserTarget.objects.create(
                        transaction_type = self.choose_random_enum(TransactionType),
                        timespan = self.choose_random_enum(Timespan),
                        amount = float(randint(0,1000000))/100,
                        currency = self.choose_random_enum(CurrencyType),
                        user_id = user
                    )
                self.create_accounts_for_user(user)
        except(IntegrityError):
            pass

        print(f'Seeding User {User.objects.count()} with accounts and transactions', end = '\r')

    def create_accounts_for_user(self, user):
        randomNumOfPotAccounts = randint(0,self.MAX_ACCOUNTS_PER_USER)
        randomNumOfBankAccount = randint(0,self.MAX_ACCOUNTS_PER_USER - randomNumOfPotAccounts)
        for i in range(0,randomNumOfPotAccounts):
            potAccount = PotAccount.objects.create(
                name = self.faker.word(),
                description = self.faker.text(),
                user_id = user,
                balance = float(randint(-1000000,1000000))/100,
                currency = self.choose_random_enum(CurrencyType)
            )
            self.create_target_for_account(potAccount)
            self.create_transactions_for_account(potAccount)
        for i in range(0,randomNumOfBankAccount):
            bankAccount = BankAccount.objects.create(
                name = self.faker.word(),
                description = self.faker.text(),
                user_id = user,
                balance = float(randint(-1000000,1000000))/100,
                currency = self.choose_random_enum(CurrencyType),
                bank_name = self.faker.word(),
                account_number = str(randint(0,9)) + "" + str(randint(1000000,9999999)),
                sort_code = str(randint(0,9)) + "" + str(randint(10000,99999)),
                iban = self.faker.name()[0] * 33,
                interest_rate = float(randint(-1000,1000))/100
            )
            self.create_target_for_account(bankAccount)
            self.create_transactions_for_account(bankAccount)

    def create_transactions_for_account(self, account):
        randomNumOfTransactions = randint(0,self.MAX_TRANSACTIONS_PER_ACCOUNT)
        oppositePartyOfTransaction = random.choice(Account.objects.all())

        if (randint(0,1) == 0):
            sender_account = oppositePartyOfTransaction
            receiver_account = account
        else:
            sender_account = account
            receiver_account = oppositePartyOfTransaction

        for i in range(0, randomNumOfTransactions):
            Transaction.objects.create(
                title = self.faker.word(),
                description = self.faker.text(),
                category = random.choice(self.categories),
                amount = float(randint(0,1000000))/100,
                currency = self.choose_random_enum(CurrencyType),
                sender_account = sender_account,
                receiver_account = receiver_account
            )


    def format_username(self, first_name, last_name):
        return f'@{first_name}{last_name}'.lower()

    def format_email(self, first_name, last_name):
        return f'{first_name}.{last_name}@gfc.org'.lower()
    
    def choose_random_enum(self, enum):
        return random.choice(list(enum))
    
    def create_target_for_account(self, account):
        if (float(randint(0,100))/100 < self.OBJECT_HAS_TARGET_PROBABILITY):
            AccountTarget.objects.create(
                transaction_type = self.choose_random_enum(TransactionType),
                timespan = self.choose_random_enum(Timespan),
                amount = float(randint(0,1000000))/100,
                currency = self.choose_random_enum(CurrencyType),
                account_id = account
            )