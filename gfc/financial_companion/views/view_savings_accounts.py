from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models import BankAccount
from ..helpers import convert_currency
from django.http import HttpRequest, HttpResponse
from currency_converter import CurrencyConverter, RateNotFoundError
from kzt_exchangerates import Rates

@login_required
def view_savings_accounts(request: HttpRequest) -> HttpResponse:
    bank_accounts: list[BankAccount] = BankAccount.objects.filter(user_id=request.user, interest_rate__gt=0)
    mainCurrency = "GBP"
    if (bank_accounts):
        mainCurrency = bank_accounts[0].currency
    otherCurrencies = []
    i = 1
    conversions: Dict[str,float] = {}
    conversions.update({str(mainCurrency) : 1.0})
    conversions.update({"GBP" : convert_currency(1, "GBP", mainCurrency)})
    while (i < len(bank_accounts)):
        currency = bank_accounts[i].currency
        conversions.update({str(currency) : convert_currency(1, currency, mainCurrency)})
        i += 1;

    return render(request, "pages/view_savings_accounts.html", {'bank_accounts': bank_accounts, 'conversion_to_main_currency':conversions, 'main_currency':mainCurrency})