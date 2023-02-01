from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.conf import settings
from ..models import Transaction, User, PotAccount
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def individual_account_view(request: HttpRequest, pk: int, filter_type: str) -> HttpResponse:
    """View to see information on individual categories"""
    user: User = request.user
    
    try:
        account = PotAccount.objects.get_subclass(id=pk, user=user)
        # print(account)
    except PotAccount.DoesNotExist:
        # print("account does not exist")
        return redirect("dashboard")


    transactions = []

    filter_send_types = ["sent", "all"]
    filter_receive_types = ["all", "received"]
    
    if not(filter_type in filter_send_types or filter_type in filter_receive_types):
        return redirect('dashboard')

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

    return render(request, "pages/individual_account.html", {"account": account, 'transactions': listOfTransactions})

@login_required
def individual_account_redirect(request: HttpRequest, pk: int) -> HttpResponse:
    return redirect('individual_account', pk = pk, filter_type="all")