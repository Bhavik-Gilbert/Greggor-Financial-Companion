from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models import Transaction, PotAccount
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.conf import settings

@login_required
def view_users_transactions(request: HttpRequest, filter_type : str) -> HttpResponse:
    user = request.user
    user_accounts = PotAccount.objects.filter(user = user.id)
    transactions = []

    filter_send_types = ["sent", "all"]
    filter_receive_types = ["all", "received"]
    
    if not(filter_type in filter_send_types or filter_type in filter_receive_types):
        return redirect('dashboard')

    for account in user_accounts:
        if filter_type in filter_send_types:
            transactions = [*transactions, *Transaction.objects.filter(sender_account=account)]
        if filter_type in filter_receive_types:
            transactions = [*transactions, *Transaction.objects.filter(receiver_account=account)]
    
    page = request.GET.get('page', settings.NUMBER_OF_TRANSACTIONS)
    paginator = Paginator(transactions, 10)
    try:
        listOfTransactions = paginator.page(page)
    except PageNotAnInteger:
        listOfTransactions = paginator.page(1)
    except EmptyPage:
        listOfTransactions = paginator.page(paginator.num_pages)
    
    return render(request, "pages/display_transactions.html", {'transactions': listOfTransactions})

@login_required
def view_users_transactions_redirect(request: HttpRequest) -> HttpResponse:
    return redirect('view_transactions', filter_type="all")

@login_required
def filter_transaction_request(request):
    if 'sent' in request.POST:
        return redirect(reverse('view_transactions', kwargs={'filter_type': "sent"}))
    elif 'received' in request.POST:
        return redirect(reverse('view_transactions', kwargs={'filter_type': "received"}))
    elif 'all' in request.POST:
        return redirect(reverse('view_transactions', kwargs={'filter_type': "all"}))
    else:
        return redirect('dashboard')


