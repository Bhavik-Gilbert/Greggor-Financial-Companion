from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from financial_companion.forms import JoinUserGroupForm
from django.contrib.auth.decorators import login_required
from ..models import UserGroup, User


@login_required
def remove_user_from_user_group_view(request: HttpRequest, group_pk: int, user_pk: int) -> HttpResponse:
    """View to remove a user from user group"""
    try:
        current_user_group: UserGroup = UserGroup.objects.get(
            id=group_pk)
    except Exception:
        messages.add_message(
            request,
            messages.WARNING,
            "Failed to identify user group")
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
                            pk=current_user_group.id)
    
    if(current_user_group.members.contains(user)):
        current_user_group.remove_member(user)
        messages.add_message(
            request,
            messages.SUCCESS,
            "Successfully removed user from user group")
        return redirect('individual_group',
                            pk=current_user_group.id)
    else:
        messages.add_message(
            request,
            messages.WARNING,
            "This user is not currently a member of this group")
        return redirect('individual_group',
                            pk=current_user_group.id)
    

    


