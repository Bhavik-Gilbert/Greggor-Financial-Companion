from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from financial_companion.models import Account, PotAccount, BankAccount, Transaction, AbstractTransaction
from ..helpers import get_data_for_account_projection
from django.contrib.auth.decorators import login_required


@login_required
def dashboard_view(request: HttpRequest) -> HttpResponse:

    user = request.user

    user_accounts = PotAccount.objects.filter(user=user.id)
    user_transactions = []
    for account in user_accounts:
        user_transactions = [
            *
            user_transactions,
            *
            Transaction.objects.filter(
                sender_account=account),
            *
            Transaction.objects.filter(
                receiver_account=account)]

    recent_transactions = user_transactions[0:3]

    context = {
        'accounts': user_accounts,
        'recent': recent_transactions,
    }

    context.update(get_data_for_account_projection(user))

    return render(request, "pages/dashboard.html", context)
