from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from ..helpers import offline_required, MonetaryAccountType

# def get_monetary_form(account_type: str, *form_args, **form_kwargs):
#     if account_type == MonetaryAccountType.BANK:
#         return BankFrom(form_args, form_kwargs), MonetaryAccountType.BANK
#     else:
#         return PotForm(form_args, form_kwargs), MonetaryAccountType.POT
        
# @offline_required
def add_monetary_account_view(request: HttpRequest) -> HttpResponse:
    """View to add monetary account"""
    
    # form, account_type = get_monetary_form(MonetaryAccountType.POT)
    account_type = MonetaryAccountType.POT # TODO: remove temp code

    if request.method == "POST":
        if "account_type" in request.POST: 
            # set form to account type
            # form, account_type = get_monetary_form(request.POST["account_type"])

            account_type = request.POST["account_type"] # TODO: remove temp code
        # elif "submit_type" in request.POST:
        #     # get form from request and check form
        #     form, account_type = get_monetary_form(request.POST["submit_type"], request.POST)
            
        
    return render(request, "pages/monetary_accounts_form.html", {
        "form_toggle": True,
        "account_type": account_type,
        "monetary_account_types": MonetaryAccountType
        # "form": form
        })