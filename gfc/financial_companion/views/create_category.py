from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from financial_companion.forms import CategoryForm
from django.contrib.auth.decorators import login_required

@login_required
def create_category_view(request: HttpRequest) -> HttpResponse:
    """View to allow users to create a category"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            user = form.save(request.user)
            return redirect('dashboard')
    else:
        form = CategoryForm()
    return render(request, "pages/create_category.html", {'form': form, "form_toggle": True})
    