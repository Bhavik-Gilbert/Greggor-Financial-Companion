from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from ..models import User, UserGroup
from ..forms import AddUserToUserGroupForm
from ..helpers import paginate, get_sorted_members_based_on_completed_targets
from typing import Union
from django.db.models import QuerySet
from django.core.paginator import Page


@login_required
def individual_group_view(request: HttpRequest, pk: int,
                          leaderboard: str = "False") -> HttpResponse:
    """View to see information on individual group"""
    try:
        group: UserGroup = UserGroup.objects.get(id=pk)
    except UserGroup.DoesNotExist:
        return redirect("dashboard")
    else:
        user: User = request.user
        members: QuerySet[User] = group.members.all()
        members_list: list[User] = list(members)
        sorted_members_list: list[User] = sorted(
            members_list, key=lambda x: x.id)
        is_owner: bool = (group.owner_email == user.email)
        owners_email: str = group.owner_email
        count: int = group.members_count()
        form: AddUserToUserGroupForm = AddUserToUserGroupForm()

        if leaderboard == "True":
            sorted_members_with_stats: list[User] = get_sorted_members_based_on_completed_targets(
                sorted_members_list)
            if count > 0:
                pagenated_members_list: Page = paginate(
                    request.GET.get('page', 1), sorted_members_with_stats)
        else:
            if count > 0:
                pagenated_members_list: Page = paginate(
                    request.GET.get('page', 1), sorted_members_list)

        return render(request, "pages/individual_group.html",
                      {
                          "group": group,
                          "members": pagenated_members_list,
                          "is_owner": is_owner,
                          "owners_email": owners_email,
                          "count": count,
                          "add_user_form": form,
                          "leaderboard": leaderboard == "True"
                      })
