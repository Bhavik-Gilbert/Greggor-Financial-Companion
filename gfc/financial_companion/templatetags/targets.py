from django import template
import financial_companion.models as fcmodels
from financial_companion.helpers import timespan_map
import datetime
register = template.Library()


@register.filter
def get_completeness(current):
    transactions = []

    if isinstance(current, fcmodels.CategoryTarget):
        transactions = get_category_transactions(current)
    elif isinstance(current, fcmodels.AccountTarget):
        transactions = get_account_transactions(current)
    elif isinstance(current, fcmodels.UserTarget):
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
        # print("completeness")
        # print(completeness)
        return round(completeness, 2)


def get_category_transactions(current):
    return current.category.get_category_transactions()


def get_account_transactions(current):
    return current.account.get_account_transactions()


def get_user_transactions(current):
    return current.user.get_user_transactions()

def get_overall_completeness(targets):
    overall_completeness = 0
    count = len(targets)
    if count == 0:
        return 0
    for target in targets:
        overall_completeness = overall_completeness + get_completeness(target)
    return overall_completeness/count

@register.filter
def get_edit_url(target):
    return "edit_" + target.getModelName() + "_target"

@register.filter
def get_delete_url(target):
    return "delete_" + target.getModelName() + "_target"
