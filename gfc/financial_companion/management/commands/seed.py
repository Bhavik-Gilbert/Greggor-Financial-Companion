""" Seeder CLass to add objects to Database"""
from django.core.management.base import BaseCommand, CommandError
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
from django.db.models import QuerySet
from django.db import models
import os
from datetime import datetime, date, timedelta, timezone
from random import randint, random
import random
from financial_companion.helpers import (
    TransactionType, CurrencyType, Timespan,
    get_random_invite_code,
    check_within_date_range, timespan_map
)
from financial_companion.scheduler import (
    create_monthly_newsletter_scheduler,
    create_bank_account_interest_scheduler,
    create_recurring_transactions_scheduler
)
from typing import Any


class Command(BaseCommand):
    """Database Seeder"""
    PASSWORD: str = "Password123"
    # MINIMUM OF FOUR PREDEFINED USERS ARE CREATED IRRESPECTIVE OF VALUE
    USER_COUNT: int = 6
    MAX_ACCOUNTS_PER_USER: int = 5
    MAX_TRANSACTIONS_PER_ACCOUNT: int = 5
    MAX_NUMBER_OF_CATEGORIES: int = 10
    MAX_NUMBER_OF_BASIC_ACCOUNTS_PER_USER: int = 3
    OBJECT_HAS_TARGET_PROBABILITY: int = 0.6
    MAX_NUMBER_OF_GROUPS: int = 5
    MAX_NUMBER_OF_RECURRING_TRANSACTIONS: int = 2

    def __init__(self) -> None:
        super().__init__()
        self.faker: Faker = Faker("en_US")

    def handle(self, *args: list[Any], **options: dict[Any, Any]) -> None:
        """Seeds Database"""
        self.create_users()
        self.create_quiz_questions()
        self.create_user_groups()
        self.create_schedulers()
        print("SEEDING COMPLETE")

    def create_schedulers(self) -> None:
        """Creates scheduler objects and saves them in database"""
        print(f'Seeding Scheduler Monthly Newsletter{30 * " "}', end='\r')
        create_monthly_newsletter_scheduler()
        print(f'Seeding Scheduler Bank Accounts Interest{30 * " "}', end='\r')
        create_bank_account_interest_scheduler()
        print(f'Seeding Scheduler Recurring Transactions{30 * " "}', end='\r')
        create_recurring_transactions_scheduler()
        print(f"SCHEDULERS SEEDED{30 * ' '}")

    def create_categories(self, user: User) -> QuerySet[Category]:
        """Creates a random number of categories and saves them in database"""
        random_number_of_categories: int = randint(
            3, self.MAX_NUMBER_OF_CATEGORIES)
        categories: QuerySet[Category] = []
        for i in range(0, random_number_of_categories):
            category: Category = Category.objects.create(
                user=user,
                name=self.faker.word(),
                description=self.faker.text()
            )
            if (float(randint(0, 100)) / 100 <
                    self.OBJECT_HAS_TARGET_PROBABILITY):
                CategoryTarget.objects.create(
                    target_type=self._choose_random_enum(TransactionType),
                    timespan=self._choose_random_enum(Timespan),
                    amount=float(randint(0, 1000000)) / 100,
                    currency=self._choose_random_enum(CurrencyType),
                    category=category
                )
            categories.append(category)
        return categories

    def create_users(self) -> None:
        """Creates users and saves them in database"""
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

    def create_single_user(self, first_name: str, last_name: str, password: str, admin_status: bool) -> None:
        """
        Creates a single user alongside a random number of account accounts 
        and saves them in the database
        """
        try:
            user: User = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=self._format_username(first_name, last_name),
                email=self._format_email(first_name, last_name),
                password=password,
                bio=self.faker.text(),
                is_staff=admin_status,
                is_superuser=admin_status
            )
            if not admin_status:
                categories: Category = self.create_categories(user)
                if (float(randint(0, 100)) / 100 <
                        self.OBJECT_HAS_TARGET_PROBABILITY):
                    UserTarget.objects.create(
                        target_type=self._choose_random_enum(
                            TransactionType),
                        timespan=self._choose_random_enum(Timespan),
                        amount=float(randint(0, 1000000)) / 100,
                        currency=self._choose_random_enum(CurrencyType),
                        user=user
                    )
                self.create_accounts_for_user(user, categories)
        except (IntegrityError):
            pass

        print(
            f'Seeding User {User.objects.count() + 1} with accounts and transactions',
            end='\r')

    def create_accounts_for_user(self, user: User, categories: QuerySet[Category]) -> None:
        """
        Creates a random number of accounts for a given user, 
        alongside their targets, transactions and recurring transactions,
        and saves them to the database
        """
        random_number_of_basic_accounts: int = randint(
            1, self.MAX_NUMBER_OF_BASIC_ACCOUNTS_PER_USER)
        random_number_of_pot_accounts: int = randint(
            1, self.MAX_ACCOUNTS_PER_USER - 1)
        random_number_of_bank_accounts: int = max(
            1, 
            randint(0, (self.MAX_ACCOUNTS_PER_USER - random_number_of_pot_accounts))
        )

        for i in range(0, random_number_of_basic_accounts):
            regular_account: Account = Account.objects.create(
                name=self.faker.word(),
                description=self.faker.text(),
                user=user
            )

        for i in range(0, random_number_of_pot_accounts):
            pot_account: PotAccount = PotAccount.objects.create(
                name=self.faker.word(),
                description=self.faker.text(),
                user=user,
                balance=float(randint(-1000000, 1000000)) / 100,
                currency=self._choose_random_enum(CurrencyType)
            )
            self.create_target_for_account(pot_account)
            self.create_transactions_for_account(pot_account, categories)
            self.create_recurring_transactions_for_account(
                pot_account, categories)

        for i in range(0, random_number_of_bank_accounts):
            bank_account: BankAccount = BankAccount.objects.create(
                name=self.faker.word(),
                description=self.faker.text(),
                user=user,
                balance=float(randint(-1000000, 1000000)) / 100,
                currency=self._choose_random_enum(CurrencyType),
                bank_name=self.faker.word(),
                account_number=str(randint(0, 9)) + "" +
                str(randint(1000000, 9999999)),
                sort_code=str(randint(0, 9)) + "" + str(randint(10000, 99999)),
                iban=self.faker.name()[0] * 33,
                interest_rate=float(randint(-50, 1000)) / 100
            )
            self.create_target_for_account(bank_account)
            self.create_transactions_for_account(bank_account, categories)
            self.create_recurring_transactions_for_account(
                pot_account, categories)

    def create_transactions_for_account(self, account: Account, categories: QuerySet[Category]) -> None:
        """
        Create a random number of transactions for a given account
        and save it to the database
        """
        random_number_of_transactions: int = randint(
            0, self.MAX_TRANSACTIONS_PER_ACCOUNT)
        opposite_party_of_transaction: Account = random.choice(
            Account.objects.filter(~Q(id=account.id), user=account.user))

        if (randint(0, 1) == 0):
            sender_account: Account = opposite_party_of_transaction
            receiver_account: Account = account
        else:
            sender_account: Account = account
            receiver_account: Account = opposite_party_of_transaction

        for i in range(0, random_number_of_transactions):
            Transaction.objects.create(
                title=self.faker.word(),
                description=self.faker.text(),
                category=random.choice(categories),
                amount=float(randint(0, 1000000)) / 100,
                currency=self._choose_random_enum(CurrencyType),
                sender_account=sender_account,
                receiver_account=receiver_account
            )

    def _format_username(self, first_name: str, last_name: str) -> str:
        return f'@{first_name}{last_name}'.lower()

    def _format_email(self, first_name, last_name) -> str:
        return f'{first_name}.{last_name}@gfc.org'.lower()

    def _choose_random_enum(self, enum: models.TextChoices) -> str:
        return random.choice(list(enum))

    def _generate_start_date(self, interval: int, number_of_intervals: int) -> date:
        """Get start date from interval"""
        total_days: int = interval * number_of_intervals
        start_time: datetime = datetime.now() - timedelta(days=total_days)
        return start_time.date()

    def _generate_random_end_date(self) -> date:
        """Generate random end date"""
        start_date: datetime = datetime.now()
        end_date: datetime = start_date + timedelta(days=1000)
        random_date: datetime = start_date + \
            (end_date - start_date) * random.random()
        return random_date.date()

    def create_target_for_account(self, account: Account) -> None:
        """Creates a target for a given account and stores it in the database"""
        if (float(randint(0, 100)) / 100 < self.OBJECT_HAS_TARGET_PROBABILITY):
            AccountTarget.objects.create(
                target_type=self._choose_random_enum(TransactionType),
                timespan=self._choose_random_enum(Timespan),
                amount=float(randint(0, 1000000)) / 100,
                currency=self._choose_random_enum(CurrencyType),
                account=account
            )

    def create_quiz_questions(self) -> None:
        """Creates the quiz questions and stores it in the database"""
        question_path: os.path = os.path.join(
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
        """
        Create a random number of user groups and save them to the database
        """
        random_number_of_groups: int = randint(1, self.MAX_NUMBER_OF_GROUPS)
        owner: User = User.objects.get(username='@johndoe')
        for i in range(0, random_number_of_groups):
            UserGroup.objects.create(
                name=self.faker.word(),
                description=self.faker.text(),
                invite_code=get_random_invite_code(8),
                owner_email=owner.email
            )
        all_groups: QuerySet[UserGroup] = UserGroup.objects.all()
        for group in all_groups:
            group.members.set(User.objects.all())

        print("USERGROUPS SEEDED")

    def create_recurring_transactions_for_account(self, account: Account, categories: QuerySet[Category]) -> None:
        """
        Create a random number of recurring transactions with transactions
        for a given account and save it to the database
        """
        random_number_of_recurring_transactions: int = randint(
            0, self.MAX_NUMBER_OF_RECURRING_TRANSACTIONS)
        opposite_party_of_transaction: Account = random.choice(
            Account.objects.filter(~Q(id=account.id), user=account.user))
        random_number_of_transactions: int = randint(0, 10)

        if (randint(0, 1) == 0):
            sender_account: Account = opposite_party_of_transaction
            receiver_account: Account = account
        else:
            sender_account: Account = account
            receiver_account: Account = opposite_party_of_transaction

        for i in range(0, random_number_of_recurring_transactions):
            interval: Timespan = self._choose_random_enum(Timespan)
            start_date: date = self._generate_start_date(
                timespan_map[interval], random_number_of_transactions)

            recurring_transaction: RecurringTransaction = RecurringTransaction.objects.create(
                title=self.faker.word(),
                description=self.faker.text(),
                category=random.choice(categories),
                amount=float(randint(0, 1000000)) / 100,
                currency=self._choose_random_enum(CurrencyType),
                sender_account=sender_account,
                receiver_account=receiver_account,
                start_date=start_date,
                end_date=self._generate_random_end_date(),
                interval=interval
            )

            current_date: date = recurring_transaction.start_date
            while check_within_date_range(recurring_transaction.start_date, datetime.now().date(), current_date):
                transaction: Transaction = Transaction.objects.create(
                    title=recurring_transaction.title,
                    description=recurring_transaction.description,
                    category=recurring_transaction.category,
                    amount=recurring_transaction.amount,
                    currency=recurring_transaction.currency,
                    sender_account=sender_account,
                    receiver_account=receiver_account
                )
                transaction.save()
                transaction.time_of_transaction: datetime = datetime.combine(
                    current_date, datetime.min.time()).replace(tzinfo=timezone.utc)
                transaction.save()
                recurring_transaction.add_transaction(transaction)

                current_date: date = current_date + \
                    timedelta(days=timespan_map[interval])
