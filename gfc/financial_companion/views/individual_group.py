from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.conf import settings
from ..models import User, UserGroup


@login_required
def individual_group_view(request: HttpRequest, pk: int) -> HttpResponse:
    """View to see information on individual group"""
    try:
        group: UserGroup = UserGroup.objects.get(id=pk)
    except group.DoesNotExist:
        return redirect("dashboard")
    else:
        user = request.user
        members = group.members.all()
        is_owner = (group.owner_email == user.email)
        count = group.members_count()
        return render(request, "pages/individual_group.html",
                      {"group": group, "members": members, "owner": is_owner, "count": count})
