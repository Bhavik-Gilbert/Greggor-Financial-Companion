from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models import PotAccount, BankAccount, Account, AccountTarget
from ..helpers import get_warning_messages_for_targets, paginate
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet


@login_required
def view_user_accounts(request: HttpRequest) -> HttpResponse:
    """View to view all the user's accounts"""
    all_user_accounts: QuerySet[Account] = Account.objects.filter(
        user_id=request.user)
    all_user_pot_accounts: QuerySet[PotAccount] = PotAccount.objects.filter(
        user_id=request.user)

    user_bank_accounts_only: QuerySet[BankAccount] = BankAccount.objects.filter(
        user_id=request.user)
    user_pot_accounts_only: QuerySet[PotAccount] = all_user_pot_accounts.exclude(
        pk__in=user_bank_accounts_only)
    user_accounts_only: QuerySet[Account] = all_user_accounts.exclude(
        pk__in=all_user_pot_accounts).order_by('name')
    paginated_user_accounts_only: list[Account] = paginate(request.GET.get('page', 1), user_accounts_only, 9)

    targets_for_messages: QuerySet[AccountTarget] = request.user.get_all_account_targets(
        all_user_accounts)
    request = get_warning_messages_for_targets(
        request, False, targets_for_messages)

    return render(request, "pages/view_accounts.html",
                  {
                      'accounts': paginated_user_accounts_only,
                      'pot_accounts': user_pot_accounts_only,
                      'bank_accounts': user_bank_accounts_only
                  })
