from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models import PotAccount, BankAccount
from django.http import HttpRequest, HttpResponse

@login_required
def view_user_pot_accounts(request: HttpRequest) -> HttpResponse:
    bank_accounts: list[BankAccount] = BankAccount.objects.filter(user_id=request.user)
    pot_accounts: list[PotAccount] = set(PotAccount.objects.filter(user_id=request.user)) - set(bank_accounts)

    return render(request, "pages/view_accounts.html", 
    {
        'pot_accounts': pot_accounts, 
        'bank_accounts': bank_accounts
    })
