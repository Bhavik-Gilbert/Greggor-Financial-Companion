from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from financial_companion.forms import CategoryTargetForm
from django.contrib.auth.decorators import login_required
from ..models import Category
from django.contrib import messages
from django.db import IntegrityError


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
        form = CategoryTargetForm(request.POST)
        if form.is_valid():
            try:
                form.save(current_category)
            except IntegrityError as e:
                messages.add_message(
                request,
                messages.WARNING,
                "This target can not be created as a target with the same timespan, transaction type and category exists")
                return render(request, "pages/create_targets.html",
                  {'form': CategoryTargetForm(), "form_toggle": True, 'title': title})
            else:
                return redirect('individual_category_redirect',
                            pk=current_category.id)
    else:
        form = CategoryTargetForm()
    return render(request, "pages/create_targets.html",
                  {'form': form, "form_toggle": True, 'title': title})