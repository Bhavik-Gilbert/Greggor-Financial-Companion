from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from financial_companion.models import PotAccount, Transaction, User
from financial_companion.helpers.enums import Timespan, FilterTransactionType
from ..helpers import get_data_for_account_projection, get_warning_messages_for_targets
from django.contrib.auth.decorators import login_required
from typing import Any
from django.db.models import QuerySet


@login_required
def dashboard_view(request: HttpRequest) -> HttpResponse:
    user: User = request.user
    user_accounts: QuerySet[PotAccount] = PotAccount.objects.filter(
        user=user.id)
    user_transactions: QuerySet[Transaction] = []
    for account in user_accounts:
        user_transactions: QuerySet[Transaction] = [
            *
            user_transactions,
            *
            Transaction.objects.filter(
                sender_account=account),
            *
            Transaction.objects.filter(
                receiver_account=account)]

    recent_transactions: QuerySet[Transaction] = user_transactions[0:3]

    total_spent: float = Transaction.calculate_total_amount_from_transactions(
        Transaction.get_transactions_from_time_period(
            Timespan.MONTH, request.user, FilterTransactionType.SENT
        )
    )
    total_received: float = Transaction.calculate_total_amount_from_transactions(
        Transaction.get_transactions_from_time_period(
            Timespan.MONTH, request.user, FilterTransactionType.RECEIVED
        )
    )

    context: dict[str, Any] = {
        'accounts': user_accounts,
        'recent': recent_transactions,
        'money_in': total_received,
        'money_out': total_spent,
    }

    request: HttpRequest = get_warning_messages_for_targets(request)

    context.update(get_data_for_account_projection(user))

    return render(request, "pages/dashboard.html", context)
