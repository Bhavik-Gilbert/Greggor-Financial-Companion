from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from financial_companion.forms import CategoryForm
from django.contrib.auth.decorators import login_required
from ..models import Category

@login_required
def edit_category_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to allow users to edit a category"""
     # check is id valid
    try:
         current_category: Category = Category.objects.get(id=pk, user =  request.user)
    except Exception:
        return redirect("dashboard")
    
    
    if request.method == "POST":
        form = CategoryForm(request.POST,  instance=current_category)
        if form.is_valid():
                form.save(current_user = request.user, instance=current_category)
                return redirect("dashboard")
    else:
        form = CategoryForm(instance=current_category)
        
    return render(request, "pages/create_category.html", {'form': form, "form_toggle": False})