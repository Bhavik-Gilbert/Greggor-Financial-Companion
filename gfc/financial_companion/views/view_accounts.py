from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models import PotAccount
from django.http import HttpRequest, HttpResponse

@login_required
def view_user_pot_accounts(request: HttpRequest) -> HttpResponse:
    accounts = PotAccount.objects.all()
    ownedaccounts = []
    for account in accounts:
        if account.user_id == request.user:
            ownedaccounts.append(account)
    return render(request, "pages/view_accounts.html", {'accounts': accounts})
