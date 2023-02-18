from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from financial_companion.forms import TargetForm
from django.contrib.auth.decorators import login_required
from ..models import Category, CategoryTarget
from django.contrib import messages
from django.db import IntegrityError
from financial_companion.models import CategoryTarget, Category

@login_required
def create_category_target_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to allow users to add a target to a category"""
    # check is id valid
    try:
        current_category: Category = Category.objects.get(
            id=pk, user=request.user)
    except Exception:
        return redirect("dashboard")
    title = "Category Target"
    if request.method == "POST":
        form = TargetForm(request.POST, foreign_key = current_category)
        if form.is_valid():
            try:
                form.save(CategoryTarget, "category")
            except IntegrityError as e:
                messages.add_message(
                request,
                messages.WARNING,
                "This target can not be created as a target with the same timespan, transaction type and category exists")
                return render(request, "pages/create_targets.html",
                  {'form': TargetForm(foreign_key = current_category), "form_toggle": True, 'title': title})
                  
            else:
                return redirect('individual_category_redirect',
                            pk=current_category.id)

    else:
        form = TargetForm(foreign_key = current_category)
    
    return render(request, "pages/create_targets.html",
                  {'form': form, "form_toggle": True, 'title': title})


@login_required
def edit_category_target_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to allow users to add a target to a category"""
    # check is id valid
    try:
        current_category_target: CategoryTarget = CategoryTarget.objects.get(
            id=pk)
        if current_category_target.category.user != request.user:
            return redirect("categories_list", search_name = "all")
    except Exception:
        return redirect("dashboard")
    title = "Category Target"
    if request.method == "POST":
        form = TargetForm(request.POST, instance = current_category_target)
        if form.is_valid():
            try:
                form.save(current_category_target.category, "category")
            except IntegrityError as e:
                messages.add_message(
                request,
                messages.WARNING,
                "This target can not be created as a target with the same timespan, transaction type and category exists")
                return render(request, "pages/create_targets.html",
                  {'form': TargetForm(), "form_toggle": True, 'title': title})
            else:
                return redirect('individual_category_redirect',
                            pk=current_category_target.category.id)
    else:
        form = TargetForm(instance = current_category_target)
    return render(request, "pages/create_targets.html",
                  {'form': form, "form_toggle": False, 'title': title})