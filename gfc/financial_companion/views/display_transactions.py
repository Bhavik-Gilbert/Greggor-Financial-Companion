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
        list_of_transactions = paginator.page(page)
    except PageNotAnInteger:
        list_of_transactions = paginator.page(1)
    except EmptyPage:
        list_of_transactions = paginator.page(paginator.num_pages)
    
    return render(request, "pages/display_transactions.html", {'transactions': list_of_transactions})

@login_required
def view_users_transactions_redirect(request: HttpRequest) -> HttpResponse:
    return redirect('view_transactions', filter_type="all")

@login_required
def filter_transaction_request(request, redirect_name: str):
    if 'sent' in request.POST:
        return redirect(reverse(redirect_name, kwargs={'filter_type': "sent"}))
    elif 'received' in request.POST:
        return redirect(reverse(redirect_name, kwargs={'filter_type': "received"}))
    elif 'all' in request.POST:
        return redirect(reverse(redirect_name, kwargs={'filter_type': "all"}))
    else:
        return redirect('dashboard')

@login_required
def filter_transaction_request_with_pk(request, redirect_name: str, pk: int):
    if 'sent' in request.POST:
        return redirect(reverse(redirect_name, kwargs={'pk': pk, 'filter_type': "sent"}))
    elif 'received' in request.POST:
        return redirect(reverse(redirect_name, kwargs={'pk': pk, 'filter_type': "received"}))
    elif 'all' in request.POST:
        return redirect(reverse(redirect_name, kwargs={'pk': pk, 'filter_type': "all"}))
    else:
        return redirect('dashboard')

