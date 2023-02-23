from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from financial_companion.forms import TargetForm
from django.contrib.auth.decorators import login_required
from ..models import Category, CategoryTarget, PotAccount, AccountTarget, UserTarget
from django.contrib import messages
from financial_companion.models import CategoryTarget, Category
import re


def create_target(request, Target, current_item):
    title_first_word = re.split(r"\B([A-Z])", Target.__name__)[0]
    title = f'{title_first_word} Target'
    form = TargetForm(request.POST, foreign_key=current_item, form_type = Target)
    if request.method == "POST":
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                messages.add_message(
                    request,
                    messages.WARNING,
                    f'This target can not be created as a target with the same timespan, transaction type and {title_first_word.lower()} exists')
                return render(request, "pages/create_targets.html",
                              {'form': TargetForm(foreign_key=current_item, form_type = Target), "form_toggle": True, 'title': title})

            else:
        
                return None
    else:
        form = TargetForm(foreign_key=current_item, form_type = Target)
    return render(request, "pages/create_targets.html",
                  {'form': form, "form_toggle": True, 'title': title})


@login_required
def create_category_target_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to allow users to add a target to a category"""
    # check is id valid
    try:
        current_category: Category = Category.objects.get(
            id=pk, user=request.user)
    except Exception:
        return redirect("dashboard")
    to_return = create_target(
        request,
        CategoryTarget,
        current_category)

    if to_return is None:
        return redirect('individual_category_redirect',
                        pk=current_category.id)
    else:
        return to_return


@login_required
def create_account_target_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to allow users to add a target to an account"""
    # check is id valid
    try:
        current_account: PotAccount = PotAccount.objects.get(
            id=pk, user=request.user)
    except Exception:
        return redirect("dashboard")

    to_return = create_target(
        request,
        AccountTarget,
        current_account)

    if to_return is None:
        return redirect('individual_account_redirect',
                        pk=current_account.id)
    else:
        return to_return


@login_required
def create_user_target_view(request: HttpRequest) -> HttpResponse:
    """View to allow users to add a target to a user"""
    to_return = create_target(request, UserTarget, request.user)

    if to_return is None:
        return redirect('dashboard')
    else:
        return to_return


def edit_target(request, Target, current_item, foreign_key):
    title_first_word = re.split(r"\B([A-Z])", Target.__name__)[0]
    title = f'{title_first_word} Target'
    if request.method == "POST":
        form = TargetForm(request.POST, foreign_key=foreign_key, instance=current_item,  form_type = Target)
        if form.is_valid() :
            try:
                form.save()
            except Exception as e:
                messages.add_message(
                    request,
                    messages.WARNING,
                    f'This target can not be created as a target with the same timespan, transaction type and {title_first_word.lower()} exists')
                return render(request, "pages/create_targets.html",
                              {'form': TargetForm( foreign_key=foreign_key, instance=current_item,  form_type = Target), "form_toggle": False, 'title': title})
            else:
                return None
    else:
        
        form = TargetForm( foreign_key=foreign_key, instance=current_item,  form_type = Target)
    return render(request, "pages/create_targets.html",
                  {'form': form, "form_toggle": False, 'title': title})


@login_required
def edit_category_target_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to allow users to edit a category target"""
    # check is id valid
    try:
        current_category_target: CategoryTarget = CategoryTarget.objects.get(
            id=pk)
        if current_category_target.category.user != request.user:
            return redirect("categories_list", search_name="all")
    except Exception:
        return redirect("dashboard")

    to_return = edit_target(
        request,
        CategoryTarget,
        current_category_target,
        current_category_target.category)

    if to_return is None:
        return redirect('individual_category_redirect',
                                pk=current_category_target.category.id)
    else:
        return to_return

@login_required
def edit_account_target_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to allow users to edit an account target"""
    # check is id valid
    try:
        current_account_target: AccountTarget = AccountTarget.objects.get(
            id=pk)
        if current_account_target.account.user != request.user:
            return redirect("view_accounts")
    except Exception:
        return redirect("dashboard")
    to_return = edit_target(
        request,
        AccountTarget,
        current_account_target,
        current_account_target.account)

    if to_return is None:
        return redirect('individual_account_redirect',
                        pk=current_account_target.account.id)
    else:
        return to_return

@login_required
def edit_user_target_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to allow users to edit an account target"""
    # check is id valid
    try:
        current_user_target: UserTarget = UserTarget.objects.get(
            id=pk)
        if current_user_target.user != request.user:
            return redirect("dashboard")
    except Exception:
        return redirect("dashboard")
    to_return = edit_target(
        request,
        UserTarget,
        current_user_target,
        request.user) 

    if to_return is None:
        return redirect("dashboard")
    else:
        return to_return
                