from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from ..models import Category, Transaction
from django.http import HttpRequest, HttpResponse

@login_required
def individual_category_view(request: HttpRequest, pk: int, filter_type : str) -> HttpResponse:
    return render(request, "pages/individual_category.html")
    

@login_required
def individual_category_redirect(request: HttpRequest, pk: int) -> HttpResponse:
    return redirect('individual_category', pk=pk, filter_type="all")