from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib import messages
from financial_companion.models import PotAccount, Transaction, User
from ..helpers import get_data_for_account_projection, get_warning_messages_for_targets
from django.contrib.auth.decorators import login_required
from json import loads
from typing import Union, Any
from django.db.models import QuerySet


@login_required
def dashboard_view(request: HttpRequest) -> HttpResponse:
    user: User = request.user
    user_accounts: Union[QuerySet, list[PotAccount]
                         ] = PotAccount.objects.filter(user=user.id)
    user_transactions: Union[QuerySet, list[Transaction]] = []
    for account in user_accounts:
        user_transactions: Union[QuerySet, list[Transaction]] = [
            *
            user_transactions,
            *
            Transaction.objects.filter(
                sender_account=account),
            *
            Transaction.objects.filter(
                receiver_account=account)]

    recent_transactions: Union[QuerySet,
                               list[Transaction]] = user_transactions[0:3]

    context: dict[str, Any] = {
        'accounts': user_accounts,
        'recent': recent_transactions,
    }

    request = get_warning_messages_for_targets(request)

    context.update(get_data_for_account_projection(user))

    return render(request, "pages/dashboard.html", context)
