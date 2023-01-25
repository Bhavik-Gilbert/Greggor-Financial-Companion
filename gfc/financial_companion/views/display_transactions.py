from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models import Transaction, PotAccount
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def view_users_transactions(request: HttpRequest) -> HttpResponse:
    user = request.user
    user_accounts = PotAccount.objects.filter(user_id = user.id)
    transactions = []
    for account in user_accounts:
        transactions = [*transactions, *Transaction.objects.filter(sender_account=account)]
        transactions = [*transactions, *Transaction.objects.filter(receiver_account=account)]
    
    if request.method == "POST":
        if "sent" in request.POST: 
            for account in user_accounts:
                transactions = [*transactions, *Transaction.objects.filter(sender_account=account)]
        # return render(request, "pages/display_transactions.html", {'transactions': transactions})
        elif "recieved" in request.POST:
            for account in user_accounts:
                transactions = [*transactions, *Transaction.objects.filter(receiver_account=account)]
            # return render(request, "pages/display_transactions.html", {'transactions': transactions})
    
    page = request.GET.get('page', 1)
    paginator = Paginator(transactions, 10)
    try:
        listOfTransactions = paginator.page(page)
    except PageNotAnInteger:
        listOfTransactions = paginator.page(1)
    except EmptyPage:
        listOfTransactions = paginator.page(paginator.num_pages)
    
    return render(request, "pages/display_transactions.html", {'transactions': listOfTransactions})