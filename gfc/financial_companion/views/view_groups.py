from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from ..models import UserGroup, User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from financial_companion.forms import JoinUserGroupForm
from typing import Union, Any
from django.core.paginator import Page
from django.db.models import QuerySet


@login_required
def all_groups_view(request: HttpRequest,
                    search_name: str = "all") -> HttpResponse:

    user_groups: list[UserGroup] = []
    user: User = request.user
    user_email: str = user.email
    all_groups: QuerySet[UserGroup] = UserGroup.objects.all()
    form: JoinUserGroupForm = JoinUserGroupForm()

    # need to get all the groups the user is in
    for group in all_groups:
        if group.owner_email == user_email:
            user_groups: list[UserGroup] = [*user_groups, group]
        elif group.is_member(user):
            user_groups: list[UserGroup] = [*user_groups, group]

    # handling the search
    if request.method == "POST" and "search" in request.POST:
        if request.POST["search"].strip(
        ) == "" or request.POST["search"] is None:
            return redirect("all_groups_redirect")
        else:
            return redirect("all_groups",
                            search_name=(request.POST["search"]))

    if (search_name != "all"):
        filter_groups: list[UserGroup] = []
        for group in user_groups:
            if search_name in group.name:
                filter_groups: list[UserGroup] = [*filter_groups, group]
        return render(request, "pages/all_groups.html",
                      {"groups": filter_groups, "form": form})

    return render(request, "pages/all_groups.html",
                  {"groups": user_groups, "form": form})
