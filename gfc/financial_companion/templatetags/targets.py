from django import template
import financial_companion.models as fcmodels
from financial_companion.helpers import timespan_map, TransactionType, convert_currency
import datetime
register = template.Library()


@register.filter
def get_completeness(current_target) -> float:
    """Gets and calculates the completeness of a target"""
    transactions: list[fcmodels.Transaction] = []

    if isinstance(current_target, fcmodels.CategoryTarget):
        transactions = get_category_transactions(current_target)
    elif isinstance(current_target, fcmodels.AccountTarget):
        transactions = get_account_transactions(current_target)
    elif isinstance(current_target, fcmodels.UserTarget):
        transactions = get_user_transactions(current_target)

    timespan_int: int = timespan_map[current_target.timespan]
    start_of_timespan_period: datetime.date = datetime.date.today(
    ) - datetime.timedelta(days=timespan_int)

    filtered_transactions: list[fcmodels.Transaction] = []
    for transaction in transactions:
        if transaction.time_of_transaction.date(
        ) >= start_of_timespan_period and transaction.time_of_transaction.date() <= datetime.date.today():
            filtered_transactions = [*filtered_transactions, transaction]

    total: float = 0.0

    for transaction in filtered_transactions:
        total += float(convert_currency(transaction.amount, transaction.currency, current.currency))

    amount: float = current_target.amount
    if amount == 0:
        return round(0, 2)
    
    completeness: float = (total / float(current_target.amount)) * 100
    return round(completeness, 2)


def get_category_transactions(current_target) -> list:
    """Gets the list of transactions for the targets category"""
    return current_target.category.get_category_transactions()


def get_account_transactions(current_target) -> list:
    """Gets the list of transactions for the targets account"""
    account: fcmodels.Account = current_target.account
    if current_target.target_type == TransactionType.EXPENSE:
        return account.get_account_transactions("sent")
    else:
        return account.get_account_transactions("received")


def get_user_transactions(current_target) -> list:
    """Gets the list of transactions for the targets user"""
    return current_target.user.get_user_transactions()


def get_overall_completeness(targets: list) -> float:
    """Gets mean completeness from a list of targets"""
    overall_completeness: float = 0
    count: int = len(targets)
    if count == 0:
        return 0
    for target in targets:
        if target.target_type == "income":
            overall_completeness = overall_completeness + \
                get_completeness(target)
        else:
            overall_completeness = overall_completeness + \
                (100 - get_completeness(target))
    return overall_completeness / count


@register.filter
def check_completeness_if_expense(completeness: float, target) -> float:
    """Returns completeness of target if it's an expense target"""
    if target is not None:
        if target.target_type == "expense":
            return 100 - completeness
    return completeness


@register.filter
def get_edit_url(target) -> str:
    """Get edit url name"""
    return "edit_" + target.get_model_name() + "_target"


@register.filter
def get_delete_url(target) -> str:
    """Get delete url name"""
    return "delete_" + target.get_model_name() + "_target"
