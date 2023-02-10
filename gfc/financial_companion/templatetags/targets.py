from django import template
from ..models import Transaction, CategoryTarget, AccountTarget, UserTarget
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

    total = 0.0

    for transaction in transactions:
        total += float(transaction.amount)

    completeness = (total / float(current.amount)) * 100

    # if completeness >= 100:
    #     return 100
    # else:
    #     return completeness
    print(current.amount)
    print(total)
    
    return completeness

def get_category_transactions(current: CategoryTarget):
    return current.category.get_category_transactions()

def get_account_transactions(current: AccountTarget):
    return current.account.get_account_transactions()

def get_user_transactions(current: UserTarget):
    return current.user.get_user_transactions()
