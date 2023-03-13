from django.core.management.base import BaseCommand
from faker import Faker
from financial_companion.models import (
    User, UserGroup,
    Account, PotAccount, BankAccount,
    CategoryTarget, UserTarget, AccountTarget,
    Transaction, RecurringTransaction,
    Category,
    QuizQuestion
)
from django.db.utils import IntegrityError
from django.db.models import Q
from django.conf import settings
import os
import datetime
from random import randint, random
import random
from financial_companion.helpers import TransactionType, CurrencyType, Timespan, get_random_invite_code, generate_random_end_date
from financial_companion.scheduler import create_monthly_newsletter_scheduler, create_bank_account_interest_scheduler, create_recurring_transactions_scheduler


class Command(BaseCommand):
    PASSWORD = "Password123"
    # MINIMUM OF FOUR PREDEFINED USERS ARE CREATED IRRESPECTIVE OF VARIABLE
    # VALUE
    USER_COUNT: int = 4
    MAX_ACCOUNTS_PER_USER: int = 6
    MAX_TRANSACTIONS_PER_ACCOUNT: int = 10
    MAX_NUMBER_OF_CATEGORIES: int = 10
    MAX_NUMBER_OF_BASIC_ACCOUNTS_PER_USER: int = 5
    OBJECT_HAS_TARGET_PROBABILITY: int = 0.6
    MAX_NUMBER_OF_GROUPS: int = 5
    MAX_NUMBER_OF_RECURRING_TRANSACTIONS: int = 3

    def __init__(self) -> None:
        super().__init__()
        self.faker: Faker = Faker("en_US")

    def handle(self, *args, **options) -> None:
        self.create_users()
        self.create_quiz_questions()
        self.create_user_groups()
        self.create_schedulers()
        print("SEEDING COMPLETE")

    def create_schedulers(self) -> None:
        print(f'Seeding Scheduler Monthly Newsletter{30 * " "}', end='\r')
        create_monthly_newsletter_scheduler()
        print(f'Seeding Scheduler Bank Accounts Interest{30 * " "}', end='\r')
        create_bank_account_interest_scheduler()
        print(f'Seeding Scheduler Recurring Transactions{30 * " "}', end='\r')
        create_recurring_transactions_scheduler()
        print(f"SCHEDULERS SEEDED{30 * ' '}")

    def create_categories(self, user) -> list[Category]:
        randomNumOfCategories: int = randint(3, self.MAX_NUMBER_OF_CATEGORIES)
        categories: list[Category] = []
        for i in range(0, randomNumOfCategories):
            category: Category = Category.objects.create(
                user=user,
                name=self.faker.word(),
                description=self.faker.text()
            )
            if (float(randint(0, 100)) / 100 <
                    self.OBJECT_HAS_TARGET_PROBABILITY):
                CategoryTarget.objects.create(
                    target_type=self.choose_random_enum(TransactionType),
                    timespan=self.choose_random_enum(Timespan),
                    amount=float(randint(0, 1000000)) / 100,
                    currency=self.choose_random_enum(CurrencyType),
                    category=category
                )
            categories.append(category)
        return categories

    def create_users(self) -> None:
        self.create_single_user("Michael", "Kolling", self.PASSWORD, True)
        self.create_single_user("admin", "user", self.PASSWORD, True)
        self.create_single_user("John", "Doe", self.PASSWORD, False)
        while User.objects.count() < self.USER_COUNT:
            self.create_single_user(
                self.faker.first_name(),
                self.faker.last_name(),
                self.PASSWORD,
                False)
        print("USERS SEEDED")

    def create_single_user(self, first_name, last_name,
                           password, adminStatus) -> None:
        try:
            user: User = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=self.format_username(first_name, last_name),
                email=self.format_email(first_name, last_name),
                password=password,
                bio=self.faker.text(),
                is_staff=adminStatus,
                is_superuser=adminStatus
            )
            if (not (adminStatus)):
                categories: list[Category] = self.create_categories(user)
                if (float(randint(0, 100)) / 100 <
                        self.OBJECT_HAS_TARGET_PROBABILITY):
                    UserTarget.objects.create(
                        target_type=self.choose_random_enum(
                            TransactionType),
                        timespan=self.choose_random_enum(Timespan),
                        amount=float(randint(0, 1000000)) / 100,
                        currency=self.choose_random_enum(CurrencyType),
                        user=user
                    )
                self.create_accounts_for_user(user, categories)
        except (IntegrityError):
            pass

        print(
            f'Seeding User {User.objects.count()} with accounts and transactions',
            end='\r')

    def create_accounts_for_user(self, user, categories) -> None:
        randomNumOfBasicAccounts: int = randint(
            1, self.MAX_NUMBER_OF_BASIC_ACCOUNTS_PER_USER)
        randomNumOfPotAccounts: int = randint(
            1, self.MAX_ACCOUNTS_PER_USER - 1)
        randomNumOfBankAccount: int = randint(
            1, self.MAX_ACCOUNTS_PER_USER - randomNumOfPotAccounts)

        for i in range(0, randomNumOfBasicAccounts):
            Account.objects.create(
                name=self.faker.word(),
                description=self.faker.text(),
                user=user
            )

        for i in range(0, randomNumOfPotAccounts):
            potAccount: PotAccount = PotAccount.objects.create(
                name=self.faker.word(),
                description=self.faker.text(),
                user=user,
                balance=float(randint(-1000000, 1000000)) / 100,
                currency=self.choose_random_enum(CurrencyType)
            )
            self.create_target_for_account(potAccount)
            self.create_transactions_for_account(potAccount, categories)
            self.create_recurring_transactions_for_account(
                potAccount, categories)

        for i in range(0, randomNumOfBankAccount):
            bankAccount: BankAccount = BankAccount.objects.create(
                name=self.faker.word(),
                description=self.faker.text(),
                user=user,
                balance=float(randint(-1000000, 1000000)) / 100,
                currency=self.choose_random_enum(CurrencyType),
                bank_name=self.faker.word(),
                account_number=str(randint(0, 9)) + "" +
                str(randint(1000000, 9999999)),
                sort_code=str(randint(0, 9)) + "" + str(randint(10000, 99999)),
                iban=self.faker.name()[0] * 33,
                interest_rate=float(randint(-50, 1000)) / 100
            )
            self.create_target_for_account(bankAccount)
            self.create_transactions_for_account(bankAccount, categories)
            self.create_recurring_transactions_for_account(
                potAccount, categories)

    def create_transactions_for_account(self, account, categories) -> None:
        randomNumOfTransactions: int = randint(
            0, self.MAX_TRANSACTIONS_PER_ACCOUNT)
        oppositePartyOfTransaction: Account = random.choice(
            Account.objects.filter(~Q(id=account.id)))

        if (randint(0, 1) == 0):
            sender_account: Account = oppositePartyOfTransaction
            receiver_account: Account = account
        else:
            sender_account: Account = account
            receiver_account: Account = oppositePartyOfTransaction

        for i in range(0, randomNumOfTransactions):
            Transaction.objects.create(
                title=self.faker.word(),
                description=self.faker.text(),
                category=random.choice(categories),
                amount=float(randint(0, 1000000)) / 100,
                currency=self.choose_random_enum(CurrencyType),
                sender_account=sender_account,
                receiver_account=receiver_account
            )

    def format_username(self, first_name, last_name) -> str:
        return f'@{first_name}{last_name}'.lower()

    def format_email(self, first_name, last_name) -> str:
        return f'{first_name}.{last_name}@gfc.org'.lower()

    def choose_random_enum(self, enum) -> list[enumerate]:
        return random.choice(list(enum))

    def create_target_for_account(self, account) -> None:
        if (float(randint(0, 100)) / 100 < self.OBJECT_HAS_TARGET_PROBABILITY):
            AccountTarget.objects.create(
                target_type=self.choose_random_enum(TransactionType),
                timespan=self.choose_random_enum(Timespan),
                amount=float(randint(0, 1000000)) / 100,
                currency=self.choose_random_enum(CurrencyType),
                account=account
            )

    def create_quiz_questions(self) -> None:
        question_path: str = os.path.join(
            settings.TEXT_DATA_DIRS["financial_companion"],
            f"seeder{os.sep}questions.txt")

        with open(question_path) as question_file:
            question_data_list: list[str] = question_file.readlines()
            for line_index in range(0, len(question_data_list), 7):
                question = question_data_list[line_index].strip()
                potential_answer_1: str = question_data_list[line_index + 1].strip(
                )
                potential_answer_2: str = question_data_list[line_index + 2].strip(
                )
                potential_answer_3: str = question_data_list[line_index + 3].strip(
                )
                potential_answer_4: str = question_data_list[line_index + 4].strip(
                )
                correct_answer: int = int(question_data_list[line_index + 5])

                if len(QuizQuestion.objects.filter(question=question)) == 0:
                    QuizQuestion.objects.create(
                        question=question,
                        potential_answer_1=potential_answer_1,
                        potential_answer_2=potential_answer_2,
                        potential_answer_3=potential_answer_3,
                        potential_answer_4=potential_answer_4,
                        correct_answer=correct_answer,
                        seeded=True
                    )

                print(
                    f'Seeding Question {QuizQuestion.objects.count()}',
                    end='\r')
        print("QUESTIONS SEEDED")

    def create_user_groups(self) -> None:
        randomNumOfGroups: int = randint(0, self.MAX_NUMBER_OF_GROUPS)
        owner: User = User.objects.get(username='@johndoe')
        for i in range(0, randomNumOfGroups):
            UserGroup.objects.create(
                name=self.faker.word(),
                description=self.faker.text(),
                invite_code=get_random_invite_code(8),
                owner_email=owner.email
            )
        all_groups: UserGroup = UserGroup.objects.all()
        for group in all_groups:
            group.members.set(User.objects.all())

        print("USERGROUPS SEEDED")

    def create_recurring_transactions_for_account(
            self, account, categories) -> None:
        randomNumOfRecTransactions: int = randint(
            0, self.MAX_NUMBER_OF_RECURRING_TRANSACTIONS)
        oppositePartyOfTransaction: Account = random.choice(
            Account.objects.filter(~Q(id=account.id)))
        randomNoOfTransactions: int = randint(0, 10)

        if (randint(0, 1) == 0):
            sender_account: Account = oppositePartyOfTransaction
            receiver_account: PotAccount = account
        else:
            sender_account: PotAccount = account
            receiver_account: Account = oppositePartyOfTransaction

        for i in range(0, randomNumOfRecTransactions):
            recTransaction: RecurringTransaction = RecurringTransaction.objects.create(
                title=self.faker.word(),
                description=self.faker.text(),
                category=random.choice(categories),
                amount=float(randint(0, 1000000)) / 100,
                currency=self.choose_random_enum(CurrencyType),
                sender_account=sender_account,
                receiver_account=receiver_account,
                start_date=datetime.date.today(),
                end_date=generate_random_end_date(),
                interval=self.choose_random_enum(Timespan)
            )
            for j in range(0, randomNoOfTransactions):
                transaction: Transaction = Transaction.objects.create(
                    title=recTransaction.title,
                    description=recTransaction.description,
                    category=recTransaction.category,
                    amount=recTransaction.amount,
                    currency=recTransaction.currency,
                    sender_account=sender_account,
                    receiver_account=receiver_account
                )
                transaction.save()
                recTransaction.add_transaction(transaction)
