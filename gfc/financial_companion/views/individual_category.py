from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse

from ..models import Category, Transaction, User

@login_required
def individual_category_view(request: HttpRequest, pk: int, filter_type: str) -> HttpResponse:
    """View to see information on individual categories"""
    user: User = request.user

    try:
        category: Category = Category.objects.get(id=pk, user=user)
    except Category.DoesNotExist:
        return redirect("dashboard")

    #TODO: Get filtered transactions

    return render(request, "pages/individual_category.html", {"category": category})
    

@login_required
def individual_category_redirect(request: HttpRequest, pk: int) -> HttpResponse:
    """View to redirect to see information on individual categories with base inputs"""

    return redirect('individual_category', pk=pk, filter_type="all")