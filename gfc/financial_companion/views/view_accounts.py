from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models import PotAccount, BankAccount, Account
from ..helpers import get_warning_messages_for_targets
from django.http import HttpRequest, HttpResponse


@login_required
def view_user_pot_accounts(request: HttpRequest) -> HttpResponse:
    all_user_monetary_accounts = PotAccount.objects.filter(user_id=request.user)
    bank_accounts: list[BankAccount] = BankAccount.objects.filter(
        user_id=request.user)
    pot_accounts: list[PotAccount] = all_user_monetary_accounts.exclude(
        pk__in=bank_accounts)
    all_user_non_monetary_accounts = Account.objects.filter(user__id=request.user)
    accounts: list[Account] = all_user_non_monetary_accounts.exclude(pk__in=pot_accounts)

    targetsForMessages = request.user.get_all_account_targets(
        all_user_monetary_accounts)
    request = get_warning_messages_for_targets(
        request, False, targetsForMessages)

    return render(request, "pages/view_accounts.html",
                  {
                        'accounts' : accounts,
                        'pot_accounts': pot_accounts,
                        'bank_accounts': bank_accounts
                  })
