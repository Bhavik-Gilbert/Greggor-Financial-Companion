from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from ..models import UserGroup
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from financial_companion.forms import JoinUserGroupForm


@login_required
def all_groups_view(request: HttpRequest, search_name: str) -> HttpResponse:

    user_groups = []
    user = request.user
    user_email = user.email
    all_groups = UserGroup.objects.all()
    form = JoinUserGroupForm()

    # need to get all the groups the user is in
    for group in all_groups:
        if group.owner_email == user_email:
            user_groups = [*user_groups, group]
        elif group.is_member(user):
            user_groups = [*user_groups, group]

    # handling the search
    if request.method == "POST" and "search" in request.POST:
        if request.POST["search"].strip(
        ) == "" or request.POST["search"] is None:
            return redirect("all_groups_redirect")
        else:
            return redirect("all_groups",
                            search_name=(request.POST["search"]))

    if (search_name != "all"):
        filter_groups = []
        for group in user_groups:
            if search_name in group.name:
                filter_groups = [*filter_groups, group]
        return render(request, "pages/all_groups.html",
                      {"groups": filter_groups, "form": form})


    return render(request, "pages/all_groups.html",
                  {"groups": user_groups, "form": form})


@login_required
def all_groups_redirect(request: HttpRequest) -> HttpResponse:
    """Redirect to view list of all existing categories"""

    return redirect("all_groups", search_name="all")
