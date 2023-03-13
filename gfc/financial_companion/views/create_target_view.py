from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from financial_companion.forms import TargetForm, TargetFilterForm
from django.contrib.auth.decorators import login_required
from ..models import Category, CategoryTarget, PotAccount, AccountTarget, UserTarget
from django.contrib import messages
from financial_companion.models import CategoryTarget, Category, User
from financial_companion.helpers.enums import Timespan, TransactionType, TargetType
import re


def create_target(request, Target, current_item):
    title_first_word = re.split(r"\B([A-Z])", Target.__name__)[0]
    title = f'{title_first_word} Target'
    form = TargetForm(request.POST, foreign_key=current_item, form_type=Target)
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
                              {'form': TargetForm(foreign_key=current_item, form_type=Target), "form_toggle": True, 'title': title})

            else:

                return None
    else:
        form = TargetForm(foreign_key=current_item, form_type=Target)
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
        form = TargetForm(
            request.POST,
            foreign_key=foreign_key,
            instance=current_item,
            form_type=Target)
        if form.is_valid():
            try:
                form.save()
            except Exception as e:
                messages.add_message(
                    request,
                    messages.WARNING,
                    f'This target can not be created as a target with the same timespan, transaction type and {title_first_word.lower()} exists')
                return render(request, "pages/create_targets.html",
                              {'form': TargetForm(foreign_key=foreign_key, instance=current_item, form_type=Target), "form_toggle": False, 'title': title})
            else:
                return None
    else:

        form = TargetForm(
            foreign_key=foreign_key,
            instance=current_item,
            form_type=Target)
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
    """View to allow users to edit a user target"""
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


@login_required
def delete_category_target_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to allow users to delete a category target"""
    # check is id valid
    try:
        current_category_target: CategoryTarget = CategoryTarget.objects.get(
            id=pk)
        category_id = current_category_target.category.id
        if current_category_target.category.user != request.user:
            return redirect("categories_list", search_name="all")
    except Exception:
        return redirect("dashboard")
    else:
        current_category_target.delete()
    messages.add_message(
        request,
        messages.WARNING,
        "This category target has been deleted")
    return redirect('individual_category_redirect', pk=category_id)


@login_required
def delete_account_target_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to allow users to delete an account target"""
    # check is id valid
    try:
        current_account_target: AccountTarget = AccountTarget.objects.get(
            id=pk)
        account_id = current_account_target.account.id
        if current_account_target.account.user != request.user:
            return redirect("view_accounts")
    except Exception:
        return redirect("dashboard")
    else:
        current_account_target.delete()
    messages.add_message(
        request,
        messages.WARNING,
        "This account target has been deleted")
    return redirect('individual_account_redirect',
                    pk=account_id)


@login_required
def delete_user_target_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to allow users to delete an user target"""
    # check is id valid
    try:
        current_user_target: UserTarget = UserTarget.objects.get(
            id=pk, user=request.user)
    except Exception:
        return redirect("dashboard")
    else:
        current_user_target.delete()
    messages.add_message(
        request,
        messages.WARNING,
        "This user target has been deleted")
    return redirect("dashboard")

@login_required
def view_targets(request: HttpRequest) -> HttpResponse:
    """View to allow users to view all their targets"""
    time = None
    income_or_expense = None
    target_type = None
    targets = request.user.get_all_targets()
    if request.method == "POST":
        form = TargetFilterForm(request.POST)
        if form.is_valid():
            time = form.get_time()
            income_or_expense = form.get_income_or_expense()
            target_type = form.get_target_type()
            if time is not "":
                targets = list(filter(lambda target: time == target.timespan, targets))
            if target_type is not "":
                targets = list(filter(lambda target: target_type == target.getModelName(), targets))
            if income_or_expense is not "":
                targets = list(filter(lambda target: income_or_expense == target.target_type, targets))
    form = TargetFilterForm()
    return render(request, "pages/target_table.html",
                  {'targets': targets, 'form': form})

@login_required
def filter_transaction_request(request, redirect_name: str):
    if 'account' in request.POST:
        return redirect(reverse(redirect_name, kwargs={'filter_type': "account"}))
    elif 'category' in request.POST:
        return redirect(reverse(redirect_name, kwargs={
                        'filter_type': "category"}))
    elif 'user' in request.POST:
        return redirect(reverse(redirect_name, kwargs={
                        'filter_type': "user"}))
    elif 'all' in request.POST:
        return redirect(reverse(redirect_name, kwargs={'filter_type': "all"}))
    else:
        return redirect('dashboard')
