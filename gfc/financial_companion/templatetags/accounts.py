from django import template
from ..models import accounts_model

register = template.Library()

@register.filter
def get_account_type(account):
    return account.get_type()
