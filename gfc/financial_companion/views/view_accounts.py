from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models import PotAccount, BankAccount
from ..helpers import get_warning_messages_for_targets
from django.http import HttpRequest, HttpResponse


@login_required
def view_user_pot_accounts(request: HttpRequest) -> HttpResponse:
    bank_accounts: list[BankAccount] = BankAccount.objects.filter(
        user_id=request.user)

    pot_accounts: list[PotAccount] = []
    for pot_account in PotAccount.objects.filter(user_id=request.user):
        if not any(pot_account.id ==
                   bank_account.id for bank_account in bank_accounts):
            pot_accounts = [*pot_accounts, pot_account]
    
    targetsForMessages = request.user.get_all_account_targets(pot_accounts)
    request = get_warning_messages_for_targets(request, False, targetsForMessages)

    return render(request, "pages/view_accounts.html",
                  {
                      'pot_accounts': pot_accounts,
                      'bank_accounts': bank_accounts
                  })
