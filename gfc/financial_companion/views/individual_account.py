from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from ..models import Transaction, User, PotAccount, AccountTarget
from financial_companion.helpers import TransactionType
from financial_companion.helpers import paginate


@login_required
def individual_account_view(
        request: HttpRequest, pk: int, filter_type: str) -> HttpResponse:
    """View to see information on individual categories"""
    user: User = request.user

    try:
        account: PotAccount = PotAccount.objects.get_subclass(id=pk, user=user)
    except PotAccount.DoesNotExist:
        return redirect("dashboard")

    account_targets: AccountTarget = AccountTarget.objects.filter(
        account=account).filter()

    if not (filter_type in TransactionType.get_send_list()
            or filter_type in TransactionType.get_received_list()):
        return redirect('dashboard')

    transactions: list[Transaction] = account.get_account_transactions(
        filter_type)

    list_of_transactions = paginate(request.GET.get('page', 1), transactions)

    return render(request, "pages/individual_account.html",
                  {"account": account, "account_targets": account_targets, 'transactions': list_of_transactions})


@login_required
def individual_account_redirect(request: HttpRequest, pk: int) -> HttpResponse:
    return redirect('individual_account', pk=pk, filter_type="all")
