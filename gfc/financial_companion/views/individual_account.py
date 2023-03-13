from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.conf import settings
from ..models import Transaction, User, PotAccount, AccountTarget, Account
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from financial_companion.helpers import FilterTransactionType
from financial_companion.helpers import paginate


@login_required
def individual_account_view(
        request: HttpRequest, pk: int, filter_type: str =FilterTransactionType.ALL) -> HttpResponse:
    """View to see information on individual categories"""
    user: User = request.user

    try:
        account: Account = Account.objects.get_subclass(id=pk, user=user)
    except Account.DoesNotExist:
        return redirect("dashboard")

    account_targets: AccountTarget = AccountTarget.objects.filter(
        account=account).filter()

    if not (filter_type in FilterTransactionType.get_send_list()
            or filter_type in FilterTransactionType.get_received_list()):
        return redirect('dashboard')

    transactions: list[Transaction] = account.get_account_transactions(
        filter_type)

    list_of_transactions = paginate(request.GET.get('page', 1), transactions)

    return render(request, "pages/individual_account.html",
                  {"account": account, "account_targets": account_targets, 'transactions': list_of_transactions})

