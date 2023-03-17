from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib import messages
from ..helpers import AccountType
from ..forms import MonetaryAccountForm
from ..models import PotAccount, User, Account, BankAccount
from django.contrib import messages
from django import forms


@login_required
def add_monetary_account_view(request: HttpRequest) -> HttpResponse:
    """View to add monetary account"""

    user: User = request.user
    account_type: AccountType = AccountType.REGULAR
    form: forms.ModelForm = MonetaryAccountForm(
        form_type=account_type, user=user)

    if request.method == "POST":
        if "account_type" in request.POST:
            # set form to account type
            account_type: str = request.POST["account_type"]
            form: forms.ModelForm = MonetaryAccountForm(
                form_type=account_type, user=user)
        elif "submit_type" in request.POST:
            # get form from request and check form
            account_type: str = request.POST["submit_type"]
            form: forms.ModelForm = MonetaryAccountForm(
                request.POST, form_type=account_type, user=user)
            if form.is_valid():
                form.save()
                return redirect("view_accounts")
    return render(request, "pages/monetary_accounts_form.html", {
        "form_toggle": True,
        "account_type": account_type,
        "monetary_account_types": AccountType,
        "form": form
    })


@login_required
def edit_monetary_account_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to edit monetary account"""

    # check is id valid
    try:
        this_account: Account = Account.objects.get_subclass(
            id=pk, user=request.user.id)
    except Exception:
        messages.add_message(
            request,
            messages.ERROR,
            "This account can not be edited")
        return redirect("view_accounts")

    this_bank_account_list: list[BankAccount] = BankAccount.objects.filter(
        id=pk, user=request.user.id)
    if len(this_bank_account_list) == 1:
        this_account = this_bank_account_list[0]

    user: User = request.user
    account_type: AccountType = this_account.get_type()

    # determine account type

    if request.method == "POST":
        form: forms.ModelForm = MonetaryAccountForm(
            request.POST,
            form_type=account_type,
            user=user,
            instance=this_account)
        if form.is_valid():
            form.save(instance=this_account)
            return redirect(
                "individual_account", pk=pk, filter_type="all")

    else:
        form: forms.ModelForm = MonetaryAccountForm(
            form_type=account_type, user=user, instance=this_account)
    return render(request, "pages/monetary_accounts_form.html", {
        "form_toggle": False,
        "account_type": account_type,
        "monetary_account_types": AccountType,
        "form": form
    })


@login_required
def delete_monetary_account_view(
        request: HttpRequest, pk: int) -> HttpResponse:
    """View to delete monetary account"""

    # check is id valid
    try:
        this_monetary_account: Account = Account.objects.get_subclass(
            id=pk, user=request.user)
    except Exception:
        return redirect("dashboard")
    this_monetary_account.delete()
    messages.add_message(
        request,
        messages.WARNING,
        "This account has been deleted")
    return redirect("view_accounts")
