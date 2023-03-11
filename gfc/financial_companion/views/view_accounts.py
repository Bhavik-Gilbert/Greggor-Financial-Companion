from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models import PotAccount, BankAccount, Account
from ..helpers import get_warning_messages_for_targets
from django.http import HttpRequest, HttpResponse


@login_required
def view_user_pot_accounts(request: HttpRequest) -> HttpResponse:
    all_user_accounts = Account.objects.filter(
        user_id=request.user)
    all_user_pot_accounts: list[PotAccount] = PotAccount.objects.filter(
        user_id=request.user)

    user_bank_accounts_only: list[BankAccount] = BankAccount.objects.filter(
        user_id=request.user)
    user_pot_accounts_only = all_user_pot_accounts.exclude(
        pk__in=user_bank_accounts_only)
    user_accounts_only = all_user_accounts.exclude(
        pk__in=all_user_pot_accounts)
    

    targetsForMessages = request.user.get_all_account_targets(
        all_user_accounts)
    request = get_warning_messages_for_targets(
        request, False, targetsForMessages)

    return render(request, "pages/view_accounts.html",
                  {
                      'accounts': user_accounts_only,
                      'pot_accounts': user_pot_accounts_only,
                      'bank_accounts': user_bank_accounts_only
                  })
