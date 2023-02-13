from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from ..models import Category
from django.contrib.auth.decorators import login_required
from django.urls import reverse


@login_required     
def category_list_view(request: HttpRequest, search_name: str) -> HttpResponse:
    """View to view list of existing categories"""

    if request.method == "POST" and "search" in request.POST:
        if request.POST["search"].strip() == "" or request.POST["search"] is None:
            return redirect("categories_list_redirect")
        else:
            return redirect("categories_list", search_name = (request.POST["search"]))

    if(search_name == "all"):
        categories: Category = Category.objects.filter(user = request.user)
    else:
        categories: Category = Category.objects.filter(user = request.user).filter(name__icontains = search_name)

    return render(request, "pages/category_list.html", {"categories": categories})

@login_required     
def category_list_redirect(request: HttpRequest) -> HttpResponse:
    """Redirect to view list of all existing categories"""

    return redirect("categories_list", search_name="all")