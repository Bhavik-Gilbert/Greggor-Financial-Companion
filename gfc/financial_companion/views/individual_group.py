from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.conf import settings
from ..models import User, UserGroup
from ..helpers import paginate, get_number_of_completed_targets, get_sorted_members_based_on_completed_targets


@login_required
def individual_group_view(request: HttpRequest, pk: int, leaderboard: str) -> HttpResponse:
    """View to see information on individual group"""
    try:
        group: UserGroup = UserGroup.objects.get(id=pk)
    except UserGroup.DoesNotExist:
        return redirect("dashboard")
    else:
        user = request.user
        members = group.members.all()
        is_owner = (group.owner_email == user.email)
        owners_email = group.owner_email
        count = group.members_count()

        sorted_members = []

        if leaderboard == "True":
            sorted_members = get_sorted_members_based_on_completed_targets(members)
            if count > 0:
                pagenated_members_list = paginate(
                    request.GET.get('page', 1), sorted_members)
        else:
            if count > 0:
                pagenated_members_list = paginate(
                    request.GET.get('page', 1), members)

        return render(request, "pages/individual_group.html",
                {"group": group, "members": pagenated_members_list, "is_owner": is_owner, "owners_email": owners_email, "count": count, "leaderboard": leaderboard=="True"})

@login_required
def individual_group_redirect(request: HttpRequest, pk: int) -> HttpResponse:
    return redirect('individual_group', pk=pk, leaderboard="False")
