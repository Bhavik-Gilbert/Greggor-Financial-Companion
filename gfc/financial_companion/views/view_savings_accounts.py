from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models import BankAccount
from django.http import HttpRequest, HttpResponse


@login_required
def view_savings_accounts(request: HttpRequest) -> HttpResponse:
    bank_accounts: list[BankAccount] = BankAccount.objects.filter(
        user_id=request.user, interest_rate__gt=0)
    return render(request, "pages/view_savings_accounts.html",
                  {'bank_accounts': bank_accounts})
