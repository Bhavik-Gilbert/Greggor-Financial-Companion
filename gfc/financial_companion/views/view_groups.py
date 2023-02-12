from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from ..models import UserGroup
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def all_groups_view(request: HttpRequest, search_name: str) -> HttpResponse:

    userGroups = []
    user = request.user
    userEmail = user.email
    allGroups = UserGroup.objects.all()

    # need to get all the groups the user is in
    for group in allGroups:
        if group.owner_email == userEmail:
            userGroups += group
        elif group.is_member(user):
            userGroups += group

    # handling the search
    if request.method == "POST" and "search" in request.POST:
        if request.POST["search"].strip(
        ) == "" or request.POST["search"] is None:
            return redirect("all_groups_redirect")
        else:
            return redirect("all_groups",
                            search_name=(request.POST["search"]))

    if (search_name != "all"):
        userGroups.filter(name__icontains=search_name)

    return render(request, "pages/all_groups.html", {"groups": userGroups})

@login_required
def all_groups_redirect(request: HttpRequest) -> HttpResponse:
    """Redirect to view list of all existing categories"""

    return redirect("all_groups", search_name="all")
