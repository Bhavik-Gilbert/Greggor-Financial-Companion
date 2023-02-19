from django import template
from ..models import Transaction, CategoryTarget, AccountTarget, UserTarget
from financial_companion.helpers import timespan_map
import datetime
register = template.Library()


@register.filter
def get_completeness(current):
    transactions = []

    if isinstance(current, CategoryTarget):
        transactions = get_category_transactions(current)
    elif isinstance(current, AccountTarget):
        transactions = get_account_transactions(current)
    elif isinstance(current, UserTarget):
        transactions = get_user_transactions(current)

    timespan_int = timespan_map[current.timespan]
    start_of_timespan_period = datetime.date.today(
    ) - datetime.timedelta(days=timespan_int)

    filtered_transactions = []
    for transaction in transactions:
        if transaction.time_of_transaction.date() >= start_of_timespan_period:
            filtered_transactions = [*filtered_transactions, transaction]

    total = 0.0

    for transaction in filtered_transactions:
        total += float(transaction.amount)

    amount = current.amount
    if amount == 0:
        return round(0, 2)
    else:
        completeness = (total / float(current.amount)) * 100
        return round(completeness, 2)


def get_category_transactions(current: CategoryTarget):
    return current.category.get_category_transactions()


def get_account_transactions(current: AccountTarget):
    return current.account.get_account_transactions()


def get_user_transactions(current: UserTarget):
    return current.user.get_user_transactions()
