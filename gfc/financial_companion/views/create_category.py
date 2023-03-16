from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from financial_companion.forms import CategoryForm
from django.contrib.auth.decorators import login_required
from ..models import Category
from django.contrib import messages


@login_required
def delete_category_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to allow users to delete a category"""
    # check is id valid
    try:
        current_category: Category = Category.objects.get(
            id=pk, user=request.user)
    except Exception:
        return redirect("dashboard")

    current_category.delete()
    messages.add_message(
        request,
        messages.WARNING,
        "This category has been deleted")
    return redirect("categories_list", search_name="all")


@login_required
def create_category_view(request: HttpRequest) -> HttpResponse:
    """View to allow users to create a category"""
    if request.method == 'POST':
        form: CategoryForm = CategoryForm(request.POST)
        if form.is_valid():
            user = form.save(request.user)
            return redirect("categories_list", search_name="all")
    else:
        form: CategoryForm = CategoryForm()
    return render(request, "pages/create_category.html",
                  {'form': form, "form_toggle": True})


@login_required
def edit_category_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to allow users to edit a category"""
    # check is id valid
    try:
        current_category: Category = Category.objects.get(
            id=pk, user=request.user)
    except Exception:
        return redirect("dashboard")

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=current_category)
        if form.is_valid():
            form.save(current_user=request.user, instance=current_category)
            return redirect('individual_category_redirect',
                            pk=current_category.id)
    else:
        form = CategoryForm(instance=current_category)

    return render(request, "pages/create_category.html",
                  {'form': form, "form_toggle": False})
