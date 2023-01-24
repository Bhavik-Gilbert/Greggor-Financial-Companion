from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models import Transaction, PotAccount
from django.http import HttpRequest, HttpResponse


@login_required
def view_users_transactions(request: HttpRequest) -> HttpResponse:
    user = request.user
    user_accounts = PotAccount.objects.filter(user_id = user.id)
    transactions = []
    if request.method == "POST":
        if "sent" in request.POST: 
            for account in user_accounts:
                transactions = [*transactions, *Transaction.objects.filter(sender_account=account)]
            return render(request, "pages/display_transactions.html", {'transactions': transactions})
        elif "recieved" in request.POST:
            for account in user_accounts:
                transactions = [*transactions, *Transaction.objects.filter(receiver_account=account)]
            return render(request, "pages/display_transactions.html", {'transactions': transactions})
    
    for account in user_accounts:
        transactions = [*transactions, *Transaction.objects.filter(sender_account=account)]
        transactions = [*transactions, *Transaction.objects.filter(receiver_account=account)]
    
    return render(request, "pages/display_transactions.html", {'transactions': transactions})