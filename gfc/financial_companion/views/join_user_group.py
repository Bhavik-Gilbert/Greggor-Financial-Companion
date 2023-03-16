from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from financial_companion.forms import JoinUserGroupForm
from django.contrib.auth.decorators import login_required
from ..models import UserGroup, User
from django.db.models import QuerySet
from typing import Any, Union


@login_required
def join_user_group_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form: JoinUserGroupForm = JoinUserGroupForm(request.POST)
        if form.is_valid():
            group_invite_code: str = form.cleaned_data.get('invite_code')
            try:
                user_group: UserGroup = UserGroup.objects.get(
                    invite_code=group_invite_code)
            except UserGroup.DoesNotExist:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "A group is not associated with the invite code provided")
                return redirect("all_groups_redirect")
            user: User = request.user
            if user_group.members.contains(user):
                messages.add_message(
                    request,
                    messages.ERROR,
                    "You are already a member of this group")
                return redirect("all_groups_redirect")
            user_group.add_member(user)
            messages.add_message(
                request,
                messages.SUCCESS,
                "You have successfully joined the group")
            user: User = request.user
            members: Union[QuerySet, list[User]] = user_group.members.all()
            is_owner: bool = (user_group.owner_email == user.email)
            count: int = user_group.members_count()
            return render(request, "pages/individual_group.html",
                          {"group": user_group, "members": members, "owner": is_owner, "count": count})
    else:
        return redirect("all_groups_redirect")
