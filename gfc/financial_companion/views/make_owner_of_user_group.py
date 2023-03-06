from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import UserGroup, User


@login_required
def make_owner_of_user_group_view(request: HttpRequest, group_pk: int, user_pk: int) -> HttpResponse:
    """View to make a user the owner of the user group"""
    try:
        current_user_group: UserGroup = UserGroup.objects.get(
            id=group_pk)
    except Exception:
        messages.add_message(
            request,
            messages.WARNING,
            "Failed to identify user group")
        return redirect("all_groups_redirect")
    
    if(request.user.email != current_user_group.owner_email):
        messages.add_message(
            request,
            messages.WARNING,
            "You are not the owner of that group")
        return redirect("all_groups_redirect")

    try:
        user: User = User.objects.get(
            id=user_pk)
    except Exception:
        messages.add_message(
            request,
            messages.WARNING,
            "Failed to identify user")
        return redirect('individual_group',
                            pk=current_user_group.id, leaderboard="False")
    
    if(current_user_group.members.contains(user)):
        current_user_group.make_owner(user)
        messages.add_message(
            request,
            messages.SUCCESS,
            "Successfully made user owner of user group")
        return redirect('individual_group',
                            pk=current_user_group.id, leaderboard="False")
    else:
        messages.add_message(
            request,
            messages.WARNING,
            "This user is not currently a member of this group")
        return redirect('individual_group',
                            pk=current_user_group.id, leaderboard="False")