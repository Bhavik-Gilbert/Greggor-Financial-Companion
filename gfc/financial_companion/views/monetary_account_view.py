from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..helpers import MonetaryAccountType
from ..forms import MonetaryAccountForm


# dict_monetary_account_models: dict = {
#     MonetaryAccountType.BANK: BankModel,
#     MonetaryAccountType.POT: PotModel
# } 
        
@login_required
def add_monetary_account_view(request: HttpRequest) -> HttpResponse:
    """View to add monetary account"""
    
    user = request.user
    account_type = MonetaryAccountType.POT
    form = MonetaryAccountForm(form_type=account_type, user=user)

    if request.method == "POST":
        if "account_type" in request.POST: 
            # # set form to account type
            account_type = request.POST["account_type"] 
            form = MonetaryAccountForm(form_type=account_type, user=user)
        elif "submit_type" in request.POST:
            # get form from request and check form
            account_type = request.POST["submit_type"] 
            form = MonetaryAccountForm(request.POST, form_type=account_type, user=user)
            if form.is_valid():
                form.save()
                return redirect("dashboard")
            
        
    return render(request, "pages/monetary_accounts_form.html", {
        "form_toggle": True,
        "account_type": account_type,
        "monetary_account_types": MonetaryAccountType,
        "form": form
        })
    
@login_required
def edit_monetary_account_view(request: HttpRequest, account_type: str, pk: int) -> HttpResponse:
    """View to edit monetary account"""

    # # get model type and check if type is valid
    # if account_type in dict_monetary_account_models.keys():
    #     monetary_account_model = dict_monetary_account_models.get(account_type)
    # else:
    #     return redirect("dashboard")

    # # check object exists and belongs to them
    # try:
    #      this_monetary_account = monetary_account_model.objects.get(id=pk, user_id=request.user.id)
    # except monetary_account_model.DoesNotExist:
    #     return redirect("dashboard")

    # if request.method == "POST":
    #     form, _ = get_monetary_form(account_type, request.POST, instance=this_monetary_account)

    #     # TODO: Check form is valid
    # else:
    #     form, _ = get_monetary_form(account_type, instance=this_monetary_account)
            
        
    return render(request, "pages/monetary_accounts_form.html", {
        "form_toggle": False,
        "account_type": account_type,
        "monetary_account_types": MonetaryAccountType
        # "form": form
        })