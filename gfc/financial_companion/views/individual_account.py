from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.conf import settings
from ..models import Transaction, User, PotAccount
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from financial_companion.helpers import TransactionType


@login_required
def individual_account_view(request: HttpRequest, pk: int, filter_type: str) -> HttpResponse:
    """View to see information on individual categories"""
    user: User = request.user
    
    try:
        account: PotAccount = PotAccount.objects.get_subclass(id=pk, user=user)
    except PotAccount.DoesNotExist:
        return redirect("dashboard")

    
    if not(filter_type in TransactionType.get_send_list() or filter_type in TransactionType.get_received_list()):
        return redirect('dashboard')

    transactions: list[Transaction] = account.get_account_transactions(filter_type)
    
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
