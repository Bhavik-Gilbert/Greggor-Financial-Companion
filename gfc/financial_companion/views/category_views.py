from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from ..models import Category, CategoryTarget
from ..helpers import get_warning_messages_for_targets
from django.contrib.auth.decorators import login_required


@login_required
def category_list_view(request: HttpRequest,
                       search_name: str = "all") -> HttpResponse:
    """View to view list of existing categories"""

    if request.method == "POST" and "search" in request.POST:
        if request.POST["search"].strip(
        ) == "" or request.POST["search"] is None:
            return redirect("categories_list_redirect")
        else:
            return redirect("categories_list",
                            search_name=(request.POST["search"]))

    categories: Category = None

    if (search_name == "all"):
        categories: Category = Category.objects.filter(user=request.user)
    else:
        categories: Category = Category.objects.filter(
            user=request.user).filter(
            name__icontains=search_name)
    targets_for_messages: list[CategoryTarget] = request.user.get_all_category_targets(
    )
    request: HttpRequest = get_warning_messages_for_targets(
        request, False, targets_for_messages)

    return render(request, "pages/category_list.html",
                  {"categories": categories})
