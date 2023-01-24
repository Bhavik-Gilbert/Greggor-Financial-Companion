from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from financial_companion.models import Account, PotAccount, Transaction, AbstractTransaction

def dashboard_view(request: HttpRequest) -> HttpResponse:

    user = request.user

    user_accounts = PotAccount.objects.filter(user_id = user.id)
    user_transactions = []
    for account in user_accounts:
        user_transactions = [*user_transactions, *Transaction.objects.filter(sender_account=account), *Transaction.objects.filter(receiver_account=account)]

    recent_transactions = user_transactions[0:3]

    return render(request, "pages/dashboard.html", {'accounts': user_accounts, 'recent': recent_transactions})
