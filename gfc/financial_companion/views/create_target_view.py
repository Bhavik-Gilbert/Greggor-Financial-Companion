from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from financial_companion.forms import TargetForm
from django.contrib.auth.decorators import login_required
from ..models import Category, CategoryTarget, PotAccount, AccountTarget, UserTarget
from django.contrib import messages
from django.db import IntegrityError
from financial_companion.models import CategoryTarget, Category
from financial_companion.helpers import create_target


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
        current_category,
        TargetForm)

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
        current_account,
        TargetForm)

    if to_return is None:
        return redirect('individual_account_redirect',
                        pk=current_account.id)
    else:
        return to_return


@login_required
def create_user_target_view(request: HttpRequest) -> HttpResponse:
    """View to allow users to add a target to a user"""
    to_return = create_target(request, UserTarget, request.user, TargetForm)

    if to_return is None:
        return redirect('dashboard')
    else:
        return to_return


@login_required
def edit_category_target_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to allow users to add a target to a category"""
    # check is id valid
    try:
        current_category_target: CategoryTarget = CategoryTarget.objects.get(
            id=pk)
        if current_category_target.category.user != request.user:
            return redirect("categories_list", search_name="all")
    except Exception:
        return redirect("dashboard")
    title = "Category Target"
    if request.method == "POST":
        form = TargetForm(request.POST, instance=current_category_target)
        if form.is_valid():
            try:
                form.save("category")
            except IntegrityError as e:
                messages.add_message(
                    request,
                    messages.WARNING,
                    "This target can not be created as a target with the same timespan, transaction type and category exists")
                return render(request, "pages/create_targets.html",
                              {'form': TargetForm(instance=current_category_target), "form_toggle": True, 'title': title})
            else:
                return redirect('individual_category_redirect',
                                pk=current_category_target.category.id)
    else:
        form = TargetForm(instance=current_category_target)
    return render(request, "pages/create_targets.html",
                  {'form': form, "form_toggle": False, 'title': title})
