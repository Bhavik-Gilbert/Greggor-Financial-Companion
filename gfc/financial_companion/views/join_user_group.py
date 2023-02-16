from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from financial_companion.forms import JoinUserGroupForm
from django.contrib.auth.decorators import login_required
from ..models import UserGroup


@login_required
def join_user_group_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = JoinUserGroupForm(request.POST)
        if form.is_valid():
            group_invite_code = form.cleaned_data.get('invite_code')
            try:
                user_group: UserGroup = UserGroup.objects.get(
                    invite_code=group_invite_code)
            except UserGroup.DoesNotExist:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "A group is not associated with the invite code provided")
                return redirect("all_groups_redirect")
            user = request.user
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
            return redirect("all_groups_redirect")
    else:
        return redirect("all_groups_redirect")
