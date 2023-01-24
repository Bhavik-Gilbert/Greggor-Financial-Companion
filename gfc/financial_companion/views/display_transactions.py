from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models import Transaction, PotAccount
from django.http import HttpRequest, HttpResponse


@login_required
def view_users_transactions(request: HttpRequest) -> HttpResponse:
    user = request.user
    user_accounts = PotAccount.objects.filter(user_id = user.id)
    recieved_transactions = []
    sent_transactions = []
    for account in user_accounts:
        recieved_transactions = [*user_transactions, *Transaction.objects.filter(sender_account=account)]
        sent_transactions = [*user_transactions, *Transaction.objects.filter(recieved_transactions=account)]
    return render(request, "pages/display_transactions.html", {'recieved_transactions': recieved_transactions, 'sent_transactions': sent_transactions})