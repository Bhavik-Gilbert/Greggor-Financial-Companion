from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from ..helpers import offline_required, MonetaryAccountType

# def get_monetary_account_form(account_type: str, *form_args, **form_kwargs):
#     if account_type == MonetaryAccountType.BANK:
#         return BankFrom(form_args, form_kwargs), MonetaryAccountType.BANK
#     elif account_type == MonetaryAccountType.POT:
#         return PotForm(form_args, form_kwargs), MonetaryAccountType.POT
#     else:
#         return None


# dict_monetary_account_models: dict = {
#     MonetaryAccountType.BANK: BankModel,
#     MonetaryAccountType.POT: PotModel
# } 
        
# @offline_required
def add_monetary_account_view(request: HttpRequest) -> HttpResponse:
    """View to add monetary account"""
    
    # form, account_type = get_monetary_form(MonetaryAccountType.POT)
    account_type = MonetaryAccountType.POT # TODO: remove temp code

    if request.method == "POST":
        if "account_type" in request.POST: 
            # # set form to account type
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
    
# @offline_required
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